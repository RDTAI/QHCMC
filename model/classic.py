import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np


class GeneticAlgorithmScheduler:
    def __init__(self, hospitals, schedule_df, population_size, generations, mutation_rate, a=0.2, b=0.8):
        self.hospitals = hospitals
        self.schedule_df = schedule_df
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.best_schedule = None
        self.best_G = float('-inf')
        self.best_satisfactory = float('-inf')
        self.a = a
        self.b = b

        # Define surgical time delay factors
        self.surgical_time_delay_factors = {
            'General Surgery': 0.5,
            'Obstetrics and Gynecology Surgery': 1,
            'Otorhinolaryngology Surgery': 0,
            'Ophthalmic Surgery': 0,
            'Urologic Surgery': 0.5,
            'Gastrointestinal Surgery': 1
        }

    def convert_to_datetime(self, time_str):
        return datetime.strptime(time_str, '%H:%M')

    def calculate_delay(self, start_time, original_start_time):
        return (start_time - original_start_time).total_seconds() / 3600

    def evaluate_solution(self, schedule):
        total_fatigue = 0
        total_satisfaction = 0
        for entry in schedule:
            total_fatigue += entry['Fatigue']
            total_satisfaction += entry['Satisfaction']

        G = self.a * total_satisfaction - self.b * total_fatigue
        return total_fatigue, total_satisfaction, G

    def get_next_day(self, day_str):
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_index = days_of_week.index(day_str)
        return days_of_week[(current_index + 1) % 7]

    def generate_initial_population(self):
        population = []
        for _ in range(self.population_size):
            schedule = []
            assigned_patients = set()

            doctor_workload = {doctor: 0 for hospital in self.hospitals.values() for doctor in
                               hospital['doctors'].values() for doctor in doctor}

            for _, patient_info in self.schedule_df.iterrows():
                if patient_info['Patient ID'] in assigned_patients:
                    continue

                hospital_id = random.choice(list(self.hospitals.keys()))
                surgery_type = patient_info['Surgery Type']
                available_doctors = self.hospitals[hospital_id]['doctors'].get(surgery_type, [])
                if not available_doctors:
                    continue

                original_start_time = self.convert_to_datetime(patient_info['Start Time'])
                duration_hours = int(patient_info['Duration (hours)'])
                delay = 0
                assigned = False

                while not assigned and delay <= 24:
                    final_start_time = original_start_time + timedelta(hours=delay)

                    delay_hours = (final_start_time - original_start_time).total_seconds() / 3600
                    delay_factor = self.surgical_time_delay_factors.get(surgery_type, 1)
                    delay_hours_adjusted = min(delay_hours * delay_factor, 2)
                    adjusted_duration = duration_hours + delay_hours_adjusted
                    final_end_time = final_start_time + timedelta(hours=adjusted_duration)

                    end_day = patient_info['Day']
                    if final_start_time.date() != original_start_time.date():
                        end_day = self.get_next_day(patient_info['Day'])

                    random.shuffle(available_doctors)
                    random.shuffle(self.hospitals[hospital_id]['rooms'])

                    for doctor_id in available_doctors:
                        for operating_room in self.hospitals[hospital_id]['rooms']:
                            if self.is_available(schedule, doctor_id, final_start_time, final_end_time) and \
                                    self.is_available(schedule, operating_room, final_start_time, final_end_time):

                                max_workload = random.randint(4, 8)
                                fatigue_factor = random.uniform(0.05, 0.15)
                                fatigue_influence = min(int(doctor_workload[doctor_id] * fatigue_factor),
                                                        int(duration_hours * 0.1))
                                adjusted_duration += fatigue_influence
                                if doctor_workload[doctor_id] +  adjusted_duration > max_workload:
                                    break_duration_hours = random.randint(1, 1)

                                    break_start_time = final_end_time
                                    break_end_time = break_start_time + timedelta(hours=break_duration_hours)

                                    if self.is_available(schedule, doctor_id, break_start_time, break_end_time):
                                        schedule.append({
                                            'Patient ID': None,
                                            'Hospital': hospital_id,
                                            'Original Day': end_day,
                                            'Original Start Time': break_start_time.strftime("%H:%M"),
                                            'Original End Time': break_end_time.strftime("%H:%M"),
                                            'End Day': end_day,
                                            'Final Start Time': break_start_time.strftime("%H:%M"),
                                            'Final End Time': break_end_time.strftime("%H:%M"),
                                            'Doctor ID': doctor_id,
                                            'Operating Room': None,
                                            'Surgery Type': 'Break',
                                            'Duration (hours)': break_duration_hours,
                                            'Delay Time': 0,
                                            'Satisfaction': 0,
                                            'Fatigue': max(0,(-break_duration_hours + max_workload - 8) / 2 ) # 在休息期间减少疲劳度
                                        })

                                        doctor_workload[doctor_id] = 0

                                    continue
                                doctor_workload[doctor_id] +=  adjusted_duration
                                delay_hours = (final_start_time - original_start_time).total_seconds() / 3600
                                satisfaction = 10 - delay_hours

                                schedule.append({
                                    'Patient ID': patient_info['Patient ID'],
                                    'Hospital': hospital_id,
                                    'Original Day': patient_info['Day'],
                                    'Original Start Time': original_start_time.strftime("%H:%M"),
                                    'Original End Time': (original_start_time + timedelta(hours=duration_hours)).strftime("%H:%M"),
                                    'End Day': end_day,
                                    'Final Start Time': final_start_time.strftime("%H:%M"),
                                    'Final End Time': final_end_time.strftime("%H:%M"),
                                    'Doctor ID': doctor_id,
                                    'Operating Room': operating_room,
                                    'Surgery Type': patient_info['Surgery Type'],
                                    'Duration (hours)': adjusted_duration,
                                    'Delay Time':delay_hours,
                                    'Satisfaction':satisfaction,
                                    'Fatigue': doctor_workload[doctor_id]
                                })
                                assigned_patients.add(patient_info['Patient ID'])
                                assigned = True
                                break
                        if assigned:
                            break
                    if not assigned:
                        delay += 1

                if not assigned:
                    print(f"Failed to assign Patient ID: {patient_info['Patient ID']} after evaluating all options.")

            population.append(schedule)

        return population

    def is_available(self, schedule, entity_id, start_time, end_time):
        for entry in schedule:
            entry_start_time = datetime.strptime(entry['Final Start Time'], "%H:%M")
            entry_end_time = datetime.strptime(entry['Final End Time'], "%H:%M")
            if entry['Doctor ID'] == entity_id or entry['Operating Room'] == entity_id:
                if not (entry_end_time <= start_time or entry_start_time >= end_time):
                    return False

        return True

    def crossover(self, parent1, parent2):
        cut_point = random.randint(1, len(parent1) - 1)
        child = parent1[:cut_point] + parent2[cut_point:]
        return child

    def mutate(self, schedule):
        for idx in range(len(schedule)):
            if random.random() < self.mutation_rate:
                patient = schedule[idx]
                hospital_id = random.choice(list(self.hospitals.keys()))
                surgery_type = patient['Surgery Type']
                available_doctors = self.hospitals[hospital_id]['doctors'].get(surgery_type, [])

                if available_doctors:
                    original_start_time = self.convert_to_datetime(patient['Original Start Time'])
                    duration_hours = int(patient['Delay Time'])
                    for attempt in range(4):
                        delay = random.choice([0, 1, 2])
                        final_start_time = original_start_time + timedelta(hours=delay)
                        final_end_time = final_start_time + timedelta(hours=duration_hours)

                        doctor_id = random.choice(available_doctors)
                        operating_room = random.choice(self.hospitals[hospital_id]['rooms'])

                        if self.is_available(schedule, doctor_id, final_start_time, final_end_time) and \
                                self.is_available(schedule, operating_room, final_start_time, final_end_time):
                            # 更新变异后的条目
                            schedule[idx]['Hospital'] = hospital_id
                            schedule[idx]['Final Start Time'] = final_start_time.strftime("%H:%M")
                            schedule[idx]['Final End Time'] = final_end_time.strftime("%H:%M")
                            schedule[idx]['Doctor ID'] = doctor_id
                            schedule[idx]['Operating Room'] = operating_room
                            schedule[idx]['Delay Time'] = self.calculate_delay(final_start_time, original_start_time)
                            break


    def select_parents(self, population):
        scores = [(self.evaluate_solution(schedule), schedule) for schedule in population]

        for score in scores:
            if len(score[0]) != 3:
                print("Error: score does not have three elements", score)

        scores.sort(key=lambda x: x[0][0])
        selected = [schedule for _, schedule in scores[:2]]

        return selected

    def optimize(self):
        population = self.generate_initial_population()

        for generation in range(self.generations):
            new_population = []

            for _ in range(self.population_size):
                parent1, parent2 = self.select_parents(population)
                child = self.crossover(parent1, parent2)
                self.mutate(child)
                new_population.append(child)

            population = new_population

        for schedule in population:
            total_fatigue, total_satisfaction, G = self.evaluate_solution(schedule)
            if total_satisfaction > self.best_satisfactory :
                self.best_satisfactory= total_satisfaction
                self.best_G =G
                self.best_schedule = schedule
                print(f"New Best Solution Found: Generation {generation + 1}, G :{G} , total_fatigue：{ total_fatigue}Satisfaction: {total_satisfaction}")

        if (generation + 1) % 10 == 0:
            print(f"Generation {generation + 1}/{self.generations} complete. Current Best G: {self.best_G} hours")

        return self.best_schedule, self.best_G

