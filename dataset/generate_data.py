import pandas as pd
import random
from datetime import datetime, timedelta

patient_ids = list(range(1,89))

surgery_types = {
    'GS': 'General Surgery',
    'OB/GYN': 'Obstetrics and Gynecology Surgery',
    'ENT': 'Otorhinolaryngology Surgery',
    'OS': 'Ophthalmic Surgery',
    'Uro': 'Urologic Surgery',
    'GI': 'Gastrointestinal Surgery'
}

schedule = []
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

for patient_id in patient_ids:
    random_day = random.choice(days_of_week)
    duration = random.randint(1, 3)
    surgery_type = random.choice(list(surgery_types.keys()))

    start_hour = random.randint(9, 17 - duration)
    start_time_str = f"{start_hour:02}:00"
    start_time_full = datetime.strptime(start_time_str, "%H:%M")

    end_time_full = start_time_full + timedelta(hours=duration)
    schedule.append({
        'Patient ID': patient_id,
        'Day': random_day,
        'Start Time': start_time_full.strftime("%H:%M"),
        'End Time': end_time_full.strftime("%H:%M"),
        'Duration (hours)': duration,
        'Surgery Type': surgery_types[surgery_type],
        'Emergency': 'No'
    })

df = pd.DataFrame(schedule)
num_emergency = int(len(patient_ids) * 0.05)
emergency_patients = random.sample(patient_ids, num_emergency)

for index, row in df.iterrows():
    if row['Patient ID'] in emergency_patients:
        df.loc[index, 'Emergency'] = 'Yes'

num_patient = len(df)
df.to_csv(f'base_patients_surgery_{num_patient}_schedule.csv', index=False)

print(f"Surgery schedule saved as : base_patients_surgery_{num_patient}_week_schedule.csv")
