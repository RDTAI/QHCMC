import pandas as pd
from datetime import datetime, timedelta
import random
import numpy as np


class Base:
    def __init__(self, hospitals, schedule_df):
        self.hospitals = hospitals
        self.schedule_df = schedule_df
        self.final_schedule = []
        self.doctor_workload = self.initialize_doctor_workload()
        self.assigned_patients = set()
        self.surgical_time_delay_factors = {
            'General Surgery': 0.5,
            'Obstetrics and Gynecology Surgery': 1,
            'Otorhinolaryngology Surgery': 0,
            'Ophthalmic Surgery': 0,
            'Urologic Surgery': 0.5,
            'Gastrointestinal Surgery': 1
        }


    def initialize_doctor_workload(self):
        doctor_workload = {}
        for hospital in self.hospitals.values():
            for doctors in hospital['doctors'].values():
                for doctor_id in doctors:
                    doctor_workload[doctor_id] = 0
        return doctor_workload

    def convert_to_datetime(self, time_str):
        return datetime.strptime(time_str, '%H:%M')

    def convert_day_to_weekday(self, day_str):
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return days_of_week.index(day_str)

    def get_next_day(self, day_str):
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_index = days_of_week.index(day_str)
        return days_of_week[(current_index + 1) % 7]

    def is_available(self, doctor_id, room, start_time, end_time, end_day ):
        for entry in self.final_schedule:
            entry_day = entry['End Day']
            existing_start_time = self.convert_to_datetime(entry['Final Start Time'])
            existing_end_time = self.convert_to_datetime(entry['Final End Time'])

            if entry['Doctor ID'] == doctor_id and not (
                    existing_start_time <= end_time or existing_end_time >= start_time) :
                return False

            if entry['Operating Room'] == room and not (
                    existing_start_time <= end_time or existing_end_time >= start_time):
                return False

        return True

    def allocate_schedule(self):
        for index, row in self.schedule_df.iterrows():
            patient_id = row['Patient ID']
            if patient_id in self.assigned_patients:
                continue

            original_day = row['Day']
            original_start_time_str = row['Start Time']
            original_duration = row['Duration (hours)']
            surgery_type = row['Surgery Type']

            original_start_time = self.convert_to_datetime(original_start_time_str)
            original_end_time = original_start_time + timedelta(hours=original_duration)

            final_start_time = original_start_time
            final_end_time = original_end_time

            assigned = False
            delay_hours =0
            while not assigned:
                for hospital_id, hospital in self.hospitals.items():
                    available_rooms = hospital['rooms']
                    available_doctors = hospital['doctors'][surgery_type]
                    available_doctors.sort(key=lambda doc: self.doctor_workload[doc])
                    for room in available_rooms:
                        for doctor_id in available_doctors:
                            if self.is_available(doctor_id, room, final_start_time, final_end_time, original_day):

                                duration_hours = original_duration
                                # delay_hours = (final_start_time - original_start_time).total_seconds() / 3600
                                delay_factor = self.surgical_time_delay_factors.get(surgery_type, 1)
                                delay_hours_adjusted = min(delay_hours * delay_factor, 2)
                                fatigue_factor = random.uniform(0.05, 0.15)
                                adjusted_duration = duration_hours + delay_hours_adjusted + min(int(self.doctor_workload[doctor_id] * fatigue_factor), int(original_duration * 0.1))
                                final_end_time = final_start_time + timedelta(hours=adjusted_duration)

                                last_end_time = None
                                for entry in reversed(self.final_schedule):
                                    if entry['Doctor ID'] == doctor_id:
                                        last_end_time = entry['Final End Time']
                                        break

                                if last_end_time and last_end_time == final_start_time.strftime("%H:%M"):
                                    # Continuous work, accumulate fatigue
                                    self.doctor_workload[doctor_id] += adjusted_duration
                                else:
                                    # Reset workload and then add adjusted duration
                                    self.doctor_workload[doctor_id] = adjusted_duration
                                satisfaction = self.calculate_satisfaction(delay_hours)
                                if final_start_time.date() > original_start_time.date():
                                    end_day = self.get_next_day(original_day)
                                else:
                                    end_day = original_day



                                self.final_schedule.append({
                                    'Patient ID': patient_id,
                                    'Hospital': hospital_id,
                                    'Original Day': original_day,
                                    'Original Start Time': original_start_time.strftime("%H:%M"),
                                    'Original End Time': original_end_time.strftime("%H:%M"),
                                    'End Day': end_day,
                                    'Final Start Time': final_start_time.strftime("%H:%M"),
                                    'Final End Time': final_end_time.strftime("%H:%M"),
                                    'Doctor ID': doctor_id,
                                    'Operating Room': room,
                                    'Surgery Type': surgery_type,
                                    'Duration (hours)': adjusted_duration,
                                    'Delay Time': delay_hours,
                                    'Satisfaction': satisfaction,
                                    'Fatigue': self.doctor_workload[doctor_id]
                                })
                                self.assigned_patients.add(patient_id)
                                assigned = True
                                break

                        if not assigned:
                           delay_hours +=0.25

                    if assigned:
                        break

                if not assigned:
                    final_start_time += timedelta(hours=1)
                    final_end_time += timedelta(hours=1)


    def calculate_satisfaction(self, delay_hours):
        satisfaction = 10 - delay_hours
        return max(0, satisfaction)

    def save_schedule(self, output_file):
        final_schedule_df = pd.DataFrame(self.final_schedule)
        final_schedule_df.to_csv(output_file, index=False)
        print(f"Schedule saved to '{output_file}'")

    def analyze_schedule(self):
        df = pd.DataFrame(self.final_schedule)
        total_delay_time = df['Delay Time'].sum()
        delay_time_list = df['Delay Time'].tolist()
        average_delay_time = np.mean(delay_time_list)
        median_delay_time = np.median(delay_time_list)

        satisfaction_scores = df['Satisfaction'].tolist()
        total_satisfaction = sum(satisfaction_scores)
        average_satisfaction = np.mean(satisfaction_scores)
        median_satisfaction = np.median(satisfaction_scores)

        fatigue_scores = {}
        for entry in self.final_schedule:
            doctor_id = entry['Doctor ID']
            fatigue_duration = entry['Fatigue']
            if doctor_id not in fatigue_scores:
                fatigue_scores[doctor_id] = 0
            fatigue_scores[doctor_id] += fatigue_duration

        total_fatigue = sum(fatigue_scores.values())
        average_fatigue = np.mean(list(fatigue_scores.values()))
        median_fatigue = np.median(list(fatigue_scores.values()))

        G_score = total_satisfaction - total_fatigue

        print("Average Delay Time:", average_delay_time, '(hours)')
        print("Average Satisfaction:", average_satisfaction)
        print("Average Fatigue:", average_fatigue, '(hours)')
        print("G_scores:", G_score)


