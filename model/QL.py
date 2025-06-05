import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from datetime import datetime, timedelta
from collections import deque
import random
import hashlib


class SurgerySchedulingEnv:
    def __init__(self, hospitals, schedule_df, a=1, b=1):
        self.hospitals = hospitals
        self.schedule_df = schedule_df
        self.current_index = 0
        self.final_schedule = []
        self.doctor_fatigue = {doctor_id: 0 for hospital in hospitals.values() for surgery_type, doctors in hospital['doctors'].items() for doctor_id in doctors}
        self.a = a
        self.b = b
        self.surgical_time_delay_factors = {
            'General Surgery': 0.5,
            'Obstetrics and Gynecology Surgery': 1,
            'Otorhinolaryngology Surgery': 0,
            'Ophthalmic Surgery': 0,
            'Urologic Surgery': 0.5,
            'Gastrointestinal Surgery': 1
        }
        self.best_schedule =[]
        self.best_satisfactory = float('-inf')
        self.best_G = float('-inf')

    def get_best_G(self):
        return self.best_G

    def get_final_schedule(self):
        return self.final_schedule

    def get_best_schedule(self):
        return self.best_schedule

    def convert_to_datetime(self, time_str):
        return datetime.strptime(time_str, '%H:%M')

    def get_next_day(self, day_str):
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_index = days_of_week.index(day_str)
        return days_of_week[(current_index + 1) % 7]

    def is_available(self, schedule, entity_id, start_time, end_time):
        for entry in schedule:
            entry_start_time = self.convert_to_datetime(entry['Final Start Time'])
            entry_end_time = self.convert_to_datetime(entry['Final End Time'])
            if entry['Doctor ID'] == entity_id or entry['Operating Room'] == entity_id:
                if not (entry_end_time <= self.convert_to_datetime(start_time) or entry_start_time >= self.convert_to_datetime(end_time)):
                    return False
        return True

    def reset(self):
        self.current_index = 0
        self.final_schedule = []
        self.doctor_fatigue = {doctor_id: 0 for hospital in self.hospitals.values() for surgery_type, doctors in hospital['doctors'].items() for doctor_id in doctors}
        return self.get_state()

    def step(self, action):
        i = self.current_index
        patient_info = self.schedule_df.iloc[i]
        original_start_time = self.convert_to_datetime(patient_info['Start Time'])
        duration_hours = int(patient_info['Duration (hours)'])
        surgery_type = patient_info['Surgery Type']

        hospital_id, doctor_id, operating_room = action
        assigned = False
        delay = 0
        reward =0
        satisfaction =0
        delay_hours =0
        while not assigned and delay <= 24:
            conflict = False
            final_start_time = original_start_time + timedelta(hours=delay)
            delay_hours = (final_start_time - original_start_time).total_seconds() / 3600
            delay_factor = self.surgical_time_delay_factors.get(surgery_type, 1)
            delay_hours_adjusted = min(delay_hours * delay_factor, 2)
            adjusted_duration = duration_hours + delay_hours_adjusted
            final_end_time = final_start_time + timedelta(hours=adjusted_duration)

            for scheduled in self.final_schedule:
                if (scheduled['Operating Room'] == operating_room and
                        not (self.convert_to_datetime(scheduled['Final End Time']) <= final_start_time or
                             self.convert_to_datetime(scheduled['Final Start Time']) >= final_end_time)):

                    available_actions = [act for act in self.get_available_actions(patient_info) if
                                         act[2] == operating_room]
                    if available_actions:
                        action = random.choice(available_actions)
                        hospital_id, doctor_id, operating_room = action
                        break
                elif (scheduled['Doctor ID'] == doctor_id and
                        not (self.convert_to_datetime(scheduled['Final End Time']) <= final_start_time or
                             self.convert_to_datetime(scheduled['Final Start Time']) >= final_end_time)):
                    conflict = True

                    available_actions = [act for act in self.get_available_actions(patient_info) if act[1] == doctor_id]
                    if available_actions:
                        action = random.choice(available_actions)
                        hospital_id, doctor_id, operating_room = action
                        break
            if not conflict:
                assigned = True
                fatigue_factor = random.uniform(0.05, 0.15)
                fatigue_influence = min(int(self.doctor_fatigue[doctor_id] * fatigue_factor),
                                        int(duration_hours * 0.1))
                adjusted_duration += fatigue_influence

                max_workload = random.randint(4, 8)

                if self.doctor_fatigue[doctor_id] + adjusted_duration > max_workload:
                    break_duration_hours = random.randint(1, 1)
                    self.add_break(doctor_id, break_duration_hours, final_end_time)
                    continue
                else:
                    self.doctor_fatigue[doctor_id] += adjusted_duration
                    end_day = self.get_next_day(patient_info['Day']) if final_start_time.date() != original_start_time.date() else patient_info['Day']
                    satisfaction = 10 - delay_hours
                    reward = self.calculate_reward(self.doctor_fatigue[doctor_id], satisfaction)
                    self.final_schedule.append({
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
                    'Delay Time': delay_hours,
                    'Satisfaction': satisfaction,
                    'Fatigue': self.doctor_fatigue[doctor_id]
                    })
                    self.current_index += 1
                    done = self.current_index >= len(self.schedule_df)
                    return self.get_state(), reward, done, {'delay_hours': delay_hours, 'satisfaction': satisfaction,
                                                            'fatigue': self.doctor_fatigue[doctor_id]}, action
            else:
                delay += 1
        return None, None, None,{'delay_hours': delay_hours, 'satisfaction': satisfaction,
                                                            'fatigue': self.doctor_fatigue[doctor_id]},None

    def add_break(self, doctor_id, break_duration_hours, final_end_time):
        break_start_time = final_end_time
        break_end_time = break_start_time + timedelta(hours=break_duration_hours)
        self.final_schedule.append({
            'Patient ID': None,
            'Hospital': None,
            'Original Day': None,
            'Original Start Time': break_start_time.strftime("%H:%M"),
            'Original End Time': break_end_time.strftime("%H:%M"),
            'End Day': None,
            'Final Start Time': break_start_time.strftime("%H:%M"),
            'Final End Time': break_end_time.strftime("%H:%M"),
            'Doctor ID': doctor_id,
            'Operating Room': None,
            'Surgery Type': 'Break',
            'Duration (hours)': break_duration_hours,
            'Delay Time': 0,
            'Satisfaction': 0,
            'Fatigue': max(0, (self.doctor_fatigue[doctor_id] - break_duration_hours)/2)
        })
        self.doctor_fatigue[doctor_id] = 0

    def calculate_reward(self, doctor_fatigue, satisfaction):
        if doctor_fatigue <= 4 and satisfaction >= 9:
            # print("Doctor fatigue:", doctor_fatigue, "Satisfaction:", satisfaction)
            # print("Reward: 1")
            return 1
        else:
            # print("Doctor fatigue:", doctor_fatigue, "Satisfaction:", satisfaction)
            # print("Reward: 0.2")
            return 0.2

    def get_state(self):
        if self.current_index < len(self.schedule_df):
            patient_info = self.schedule_df.iloc[self.current_index]
            return patient_info
        return None

    def get_available_actions(self, state):
        patient_info = state
        surgery_type = patient_info['Surgery Type']
        available_actions = []
        for hospital_id, hospital_data in self.hospitals.items():
            for doctor_id in hospital_data['doctors'].get(surgery_type, []):
                for room_id in hospital_data['rooms']:
                    if self.is_available(self.final_schedule, doctor_id, patient_info['Start Time'], patient_info['End Time']):
                        available_actions.append((hospital_id, doctor_id, room_id))
        return available_actions or self.generate_random_action(patient_info)

    def generate_random_action(self, patient_info):
        surgery_type = patient_info['Surgery Type']
        hospital_id = random.choice(list(self.hospitals.keys()))
        doctor_id = random.choice(self.hospitals[hospital_id]['doctors'].get(surgery_type, []))
        operating_room = random.choice(self.hospitals[hospital_id]['rooms'])
        return [(hospital_id, doctor_id, operating_room)]

    def create_action_mapping(self):
        action_mapping = {}
        action_index = 0
        for hospital_id, hospital_data in self.hospitals.items():
            for surgery_type, doctors in hospital_data['doctors'].items():
                for doctor_id in doctors:
                    for room_id in hospital_data['rooms']:
                        action_mapping[(hospital_id, doctor_id, room_id)] = action_index
                        action_index += 1
        return action_mapping

    def save_schedule(self, filename):

        schedule_df = pd.DataFrame(self.best_schedule)
        schedule_df.to_csv("results/"+filename, index=False)
        return self.best_schedule, self.best_G


class SurgerySchedulingEnvMH:
    def __init__(self, hospitals, schedule_df, a=1, b=1):
        self.hospitals = hospitals
        self.schedule_df = schedule_df
        self.current_index = 0
        self.final_schedule = []
        self.doctor_fatigue = {doctor_id: 0 for hospital in hospitals.values() for surgery_type, doctors in hospital['doctors'].items() for doctor_id in doctors}
        self.a = a
        self.b = b
        self.surgical_time_delay_factors = {
            'General Surgery': 0.5,
            'Obstetrics and Gynecology Surgery': 1,
            'Otorhinolaryngology Surgery': 0,
            'Ophthalmic Surgery': 0,
            'Urologic Surgery': 0.5,
            'Gastrointestinal Surgery': 1
        }
        self.best_schedule =[]
        self.best_satisfactory = float('-inf')
        self.best_G = float('-inf')

    def get_best_G(self):
        return self.best_G

    def get_final_schedule(self):
        return self.final_schedule

    def get_best_schedule(self):
        return self.best_schedule

    def convert_to_datetime(self, time_str):
        return datetime.strptime(time_str, '%H:%M')

    def get_next_day(self, day_str):
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_index = days_of_week.index(day_str)
        return days_of_week[(current_index + 1) % 7]

    def is_available(self, schedule, entity_id, start_time, end_time):
        for entry in schedule:
            entry_start_time = self.convert_to_datetime(entry['Final Start Time'])
            entry_end_time = self.convert_to_datetime(entry['Final End Time'])
            if entry['Doctor ID'] == entity_id or entry['Operating Room'] == entity_id:
                if not (entry_end_time <= self.convert_to_datetime(start_time) or entry_start_time >= self.convert_to_datetime(end_time)):
                    return False
        return True

    def reset(self):
        self.current_index = 0
        self.final_schedule = []
        self.doctor_fatigue = {doctor_id: 0 for hospital in self.hospitals.values() for surgery_type, doctors in hospital['doctors'].items() for doctor_id in doctors}
        return self.get_state()

    def step(self, action):
        i = self.current_index
        patient_info = self.schedule_df.iloc[i]
        original_start_time = self.convert_to_datetime(patient_info['Start Time'])
        duration_hours = int(patient_info['Duration (hours)'])
        surgery_type = patient_info['Surgery Type']

        hospital_id, doctor_id, operating_room = action
        assigned = False
        delay = 0
        reward =0
        satisfaction = 0
        delay_hours =0
        while not assigned and delay <= 24:
            conflict = False
            final_start_time = original_start_time + timedelta(hours=delay)
            delay_hours = (final_start_time - original_start_time).total_seconds() / 3600
            delay_factor = self.surgical_time_delay_factors.get(surgery_type, 1)
            delay_hours_adjusted = min(delay_hours * delay_factor, 2)
            adjusted_duration = duration_hours + delay_hours_adjusted
            final_end_time = final_start_time + timedelta(hours=adjusted_duration)

            for scheduled in self.final_schedule:
                if (scheduled['Operating Room'] == operating_room and
                        not (self.convert_to_datetime(scheduled['Final End Time']) <= final_start_time or
                             self.convert_to_datetime(scheduled['Final Start Time']) >= final_end_time)):
                    available_actions = [act for act in self.get_available_actions(patient_info) if
                                         act[2] == operating_room]
                    if available_actions:  # 如果有可用的医生
                        action = random.choice(available_actions)
                        hospital_id, doctor_id, operating_room = action
                        break
                elif (scheduled['Doctor ID'] == doctor_id and
                        not (self.convert_to_datetime(scheduled['Final End Time']) <= final_start_time or
                             self.convert_to_datetime(scheduled['Final Start Time']) >= final_end_time)):
                    conflict = True
                    # 如果医生冲突，尝试更换手术室而保留医生
                    available_actions = [act for act in self.get_available_actions(patient_info) if act[1] == doctor_id]
                    if available_actions:  # 如果有可用的手术室
                        action = random.choice(available_actions)
                        hospital_id, doctor_id, operating_room = action
                        break
            if not conflict:
                assigned = True
                fatigue_factor = random.uniform(0.05, 0.15)
                fatigue_influence = min(int(self.doctor_fatigue[doctor_id] * fatigue_factor),
                                        int(duration_hours * 0.1))
                adjusted_duration += fatigue_influence
                # self.doctor_fatigue[doctor_id] += adjusted_duration
                max_workload = random.randint(4, 6)
                # max_workload = 24
                if self.doctor_fatigue[doctor_id] + adjusted_duration > max_workload:
                    break_duration_hours = random.randint(1, 1)
                    self.add_break(doctor_id, break_duration_hours, final_end_time)
                    continue
                else:
                    self.doctor_fatigue[doctor_id] += adjusted_duration
                    end_day = self.get_next_day(patient_info['Day']) if final_start_time.date() != original_start_time.date() else patient_info['Day']
                    satisfaction = 10 - delay_hours
                    # print("patient id:",patient_info['Patient ID'],"delay hours:", delay_hours, "   satisfactory: ", satisfaction)
                    reward = self.calculate_reward(self.doctor_fatigue[doctor_id], satisfaction)
                    self.final_schedule.append({
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
                    'Delay Time': delay_hours,
                    'Satisfaction': satisfaction,
                    'Fatigue': self.doctor_fatigue[doctor_id]
                    })
                    self.current_index += 1
                    done = self.current_index >= len(self.schedule_df)
                    return self.get_state(), reward, done, {'delay_hours': delay_hours, 'satisfaction': satisfaction,
                                                            'fatigue': self.doctor_fatigue[doctor_id]}, action
            else:
                delay += 1
        return None, None, None, {'delay_hours': delay_hours, 'satisfaction': satisfaction,
                                                            'fatigue': self.doctor_fatigue[doctor_id]},None

    def add_break(self, doctor_id, break_duration_hours, final_end_time):
        break_start_time = final_end_time
        break_end_time = break_start_time + timedelta(hours=break_duration_hours)
        self.final_schedule.append({
            'Patient ID': None,
            'Hospital': None,
            'Original Day': None,
            'Original Start Time': break_start_time.strftime("%H:%M"),
            'Original End Time': break_end_time.strftime("%H:%M"),
            'End Day': None,
            'Final Start Time': break_start_time.strftime("%H:%M"),
            'Final End Time': break_end_time.strftime("%H:%M"),
            'Doctor ID': doctor_id,
            'Operating Room': None,
            'Surgery Type': 'Break',
            'Duration (hours)': break_duration_hours,
            'Delay Time': 0,
            'Satisfaction': 0,
            'Fatigue': max(0, (self.doctor_fatigue[doctor_id] - break_duration_hours)/2)
        })
        self.doctor_fatigue[doctor_id] = 0

    def calculate_reward(self, doctor_fatigue, satisfaction):
        if doctor_fatigue <= 4 and satisfaction >= 9:
            return 1
        else:
            return 0.2

    def get_state(self):
        if self.current_index < len(self.schedule_df):
            patient_info = self.schedule_df.iloc[self.current_index]
            return patient_info
        return None

    def get_available_actions(self, state):
        patient_info = state
        surgery_type = patient_info['Surgery Type']
        available_actions = []
        for hospital_id, hospital_data in self.hospitals.items():
            for doctor_id in hospital_data['doctors'].get(surgery_type, []):
                for room_id in hospital_data['rooms']:
                    if self.is_available(self.final_schedule, doctor_id, patient_info['Start Time'], patient_info['End Time']):
                        available_actions.append((hospital_id, doctor_id, room_id))
        return available_actions or self.generate_random_action(patient_info)

    def generate_random_action(self, patient_info):
        surgery_type = patient_info['Surgery Type']
        hospital_id = random.choice(list(self.hospitals.keys()))
        doctor_id = random.choice(self.hospitals[hospital_id]['doctors'].get(surgery_type, []))
        operating_room = random.choice(self.hospitals[hospital_id]['rooms'])
        return [(hospital_id, doctor_id, operating_room)]

    def create_action_mapping(self):
        action_mapping = {}
        action_index = 0
        for hospital_id, hospital_data in self.hospitals.items():
            for surgery_type, doctors in hospital_data['doctors'].items():
                for doctor_id in doctors:
                    for room_id in hospital_data['rooms']:
                        action_mapping[(hospital_id, doctor_id, room_id)] = action_index
                        action_index += 1
        return action_mapping

    def save_schedule(self, filename):
        # 将最佳调度转换为 DataFrame
        schedule_df = pd.DataFrame(self.best_schedule)
        schedule_df.to_csv("results/"+filename, index=False)

        return self.best_schedule, self.best_G  # 返回总延迟和平均满意度

class QLearningAgentMH:
    def __init__(self, state_size, action_size, action_mapping):
        self.state_size = state_size
        self.action_size = action_size
        self.q_table = np.zeros((state_size, action_size))
        self.gamma = 0.9
        self.epsilon = 1.0
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.995
        self.learning_rate = 0.1
        self.action_mapping = action_mapping #dictionary mapping actions to index

    def act(self, state, available_actions):
        if np.random.rand() <= self.epsilon:
            if available_actions:
                return random.choice(available_actions)  # Explore

        else:  # Exploit
            best_action = None
            best_q_value = float('-inf')
            for action in available_actions:
                q_value = self.q_table[self.state_to_index(state), self.action_to_index(action)]
                if q_value > best_q_value:
                    best_q_value = q_value
                    best_action = action
            return best_action
    def update_q_table(self, state_index, action_index, reward, next_state_index):
        if next_state_index is not None:
            best_next_action_index = np.argmax(self.q_table[next_state_index])
            target = reward + self.gamma * self.q_table[next_state_index, best_next_action_index]
        else:
            target = reward
        self.q_table[state_index, action_index] += self.learning_rate * (target - self.q_table[state_index, action_index])

    def state_to_index(self, state):

        features = self.extract_features(state)
        feature_string = ",".join(map(str, features))
        hash_object = hashlib.sha256(feature_string.encode())
        hash_value = int(hash_object.hexdigest(), 16)
        return hash_value % self.state_size

    def extract_features(self, state):
        try:
            surgery_type = state['Surgery Type']
            duration_hours = state['Duration (hours)']
            start_time = state['Start Time']
            emergency = 1 if state['Emergency'] == 'Yes' else 0
            return [surgery_type, duration_hours, start_time, emergency]
        except (KeyError, TypeError):
            return [0,0,0,0]

    def action_to_index(self, action):
        return self.action_mapping[action]

    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

class QLearningAgent:
    def __init__(self, state_size, action_size, action_mapping):
        self.state_size = state_size
        self.action_size = action_size
        self.q_table = np.zeros((state_size, action_size))
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.995
        self.learning_rate = 0.1
        self.action_mapping = action_mapping

    def act(self, state, available_actions):
        if np.random.rand() <= self.epsilon:
            if available_actions:
                return random.choice(available_actions)  # Explore

        else:  # Exploit
            best_action = None
            best_q_value = float('-inf')
            for action in available_actions:
                q_value = self.q_table[self.state_to_index(state), self.action_to_index(action)]
                if q_value > best_q_value:
                    best_q_value = q_value
                    best_action = action
            return best_action
    def update_q_table(self, state_index, action_index, reward, next_state_index):
        if next_state_index is not None:
            best_next_action_index = np.argmax(self.q_table[next_state_index])
            target = reward + self.gamma * self.q_table[next_state_index, best_next_action_index]
        else:
            target = reward
        self.q_table[state_index, action_index] += self.learning_rate * (target - self.q_table[state_index, action_index])

    def state_to_index(self, state):
        features = self.extract_features(state)
        feature_string = ",".join(map(str, features))
        hash_object = hashlib.sha256(feature_string.encode())
        hash_value = int(hash_object.hexdigest(), 16)
        return hash_value % self.state_size

    def extract_features(self, state):

        try:
            surgery_type = state['Surgery Type']
            duration_hours = state['Duration (hours)']
            start_time = state['Start Time']
            emergency = 1 if state['Emergency'] == 'Yes' else 0
            return [surgery_type, duration_hours, start_time, emergency]
        except (KeyError, TypeError):
            return [0,0,0,0]

    def action_to_index(self, action):
        return self.action_mapping[action]

    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

def train_agent_ql(agent, env, schedule_df, episodes=1000,a = 1,b = 1):
    episode_rewards = []
    episode_satisfaction_scores = []
    episode_fatigue_scores = []
    episode_delays = []
    episode_G_score = []

    for episode in range(episodes):
        state = env.reset()
        total_delay_hours = 0
        total_satisfaction = 0
        total_fatigue = 0
        total_reward = 0
        for i in range(len(schedule_df)):

            available_actions = env.get_available_actions(state)
            action = agent.act(state, available_actions)
            next_state, reward, done, info, action = env.step(action)
            while (action is None):
                action = agent.act(state, available_actions)
                next_state, reward, done, info, action = env.step(action)
            state_index = agent.state_to_index(state)
            next_state_index = agent.state_to_index(next_state) if next_state is not None else None
            action_index = agent.action_to_index(action)
            agent.update_q_table(state_index, action_index, reward, next_state_index)
            state = next_state
            total_delay_hours += info['delay_hours']

            total_satisfaction += info['satisfaction']
            total_fatigue += info['fatigue']
            total_reward += reward

            if done:
                break
        G_score = a * total_satisfaction - b * total_fatigue
        print(
            f"Episode {episode + 1}/{episodes}, Epsilon: {agent.epsilon:.2f}, Total Reward: "
            f"{total_reward}, Total Delay: {total_delay_hours}, Total Satisfaction: "
            f"{total_satisfaction}, Total Fatigue: {total_fatigue},G_score:{G_score} ")

        if G_score > env.best_G :
            env.best_G = G_score
            env.best_schedule = env.final_schedule

        agent.decay_epsilon()
        episode_rewards.append(total_reward)
        episode_delays.append(total_delay_hours)
        episode_satisfaction_scores.append(total_satisfaction)
        episode_fatigue_scores.append(total_fatigue)
        episode_G_score.append(G_score)

    return episode_rewards, episode_satisfaction_scores, episode_fatigue_scores, episode_G_score, episode_delays

