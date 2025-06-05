import os

import pandas as pd
import matplotlib.pyplot as plt
# 定义文件夹路径，如果不存在则创建它
output_folder = 'Gantts'
os.makedirs(output_folder, exist_ok=True)
# 定义文件路径和对应的名称
#应该每个医生3-4个手术
# 只画周六日的
file_paths = {
    # '../Final/aco_patient_and_hospital_schedule_comprehensive.csv': 'ACO',
    # '../Final/bco_patient_and_hospital_schedule_comprehensive.csv': 'BCO',
    # '../Final/gao_patient_and_hospital_schedule_comprehensive.csv': 'GAO',
    # '../Final/ica_patient_and_hospital_schedule_comprehensive.csv': 'ICA',
    '../model/Q-Learning & MH Q-Learning_patient_and_hospital_schedule_comprehensive.csv': 'MCHC Q-Learning',
    # '../model/Q-Learning_patient_and_hospital_schedule_comprehensive.csv': 'Q-Learning'
}
i=0
j=0
# 循环处理每个文件
for file_path, name in file_paths.items():
    # 读取CSV文件
    df = pd.read_csv(file_path)
    print(f"Processing file: {name}")

    # 从Monday到Sunday绘制7张图
    for day in [ 'Saturday', 'Sunday']:
        data_y = []
        day_df = df[df['End Day'] == day]

        # Combine 'End Day' with 'Final Start Time' and 'Final End Time' into full datetime
        day_df['Final Start Time'] = pd.to_datetime(day + ' ' + day_df['Final Start Time'], format='%A %H:%M')
        day_df['Final End Time'] = pd.to_datetime(day + ' ' + day_df['Final End Time'], format='%A %H:%M')

        # Drop rows with NaN Patient ID
        day_df = day_df.dropna(subset=['Patient ID'])

        # Prepare the Gantt chart
        fig, ax = plt.subplots(figsize=(14, 10))
        low_saturation_colors = [
            '#A8C6E7',  # Soft Light Blue
            '#F0B8B8',  # Soft Light Pink
            '#C0E5C4',  # Soft Light Green
            '#B7E1E4',  # Soft Light Cyan
            '#E3B8F0',  # Soft Light Purple
            '#FBE7A6'  # Soft Light Yellow
        ]

        # Create Gantt Chart
        existing_positions = []

        for index, row in day_df.iterrows():
            if row['Patient ID'] is None:
                continue  # Skip this entry if Patient ID is None
            print(i)
            i +=1
            duration = (row['Final End Time'] - row[
                'Final Start Time']).total_seconds() / 3600  # Convert duration to hours

            if duration > 0:  # Ensure valid duration
                start_hour = row['Final Start Time'].hour  # Get the hour from the datetime
                end_hour = row['Final End Time'].hour  # Get the hour from the datetime
                if start_hour >= 9 and end_hour <= 18:  # Only plot if the start hour is 9 or later
                    print(j)
                    j =j+1
                    data_y.append(f"{row['Doctor ID']}")
                    ax.barh(f"{row['Doctor ID']}",
                            duration,
                            left=start_hour,  # Use the hour as the position

                            color=low_saturation_colors[index % len(low_saturation_colors)],  # Select color
                            edgecolor=None)
                    # ax.text(start_hour ,
                    #         f"{row['Doctor ID']}",
                    #         # s = f"{row['Operating Room']}; P {int(row['Patient ID'])}",
                    #         s = f"P {int(row['Patient ID'])}",
                    #         verticalalignment='center',
                    #         fontsize=6,
                    #         color='black')  # Optional: keep the text color
                    #         # Customize the x-axis to show only hours from 9 to 23
                    # 检查该位置是否已经有文本

                    if (start_hour, f"{row['Doctor ID']}") not in existing_positions:
                        # 如果没有，则添加文本并记录位置
                        ax.text(start_hour,
                                f"{row['Doctor ID']}",
                                s=f"P {int(row['Patient ID'])}",
                                verticalalignment='center',
                                fontsize=16,
                                color='black')
                        existing_positions.append((start_hour,  f"{row['Doctor ID']}"))
                    else:
                        # 如果已有文本，可以决定不添加或处理冲突
                        print(f"{row['Doctor ID']}, {row['Final Start Time']} - {row['Final End Time']}, P {row['Patient ID']}")
                        print("这个位置已包含文本，跳过或更新")
        print("existing_positions:",existing_positions)
        ax.set_xticks(range(9, 19))  # Set x-ticks as integers 9-23 for hours
        ax.set_xticklabels(["9:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00"],fontsize=20)  # Label ticks as time in hours
        ax.tick_params(axis='y', labelsize=20)
        # Set title and labels
        plt.title(f'{name} - {day} Surgical Schedule Gantt Chart', fontsize=30)
        plt.xlabel(f'Time of {day}', fontsize=30)
        plt.ylabel('Surgeries (Doctor ID)', fontsize=30)
        plt.tight_layout()
        # 保存图像
        filename = f"{name}_{day}_Gantt_Chart_1.png"  # 根据文件名和日期生成图像名称
        file_path = os.path.join(output_folder, filename)  # 生成完整的文件路径

        plt.savefig(file_path)
        print(f"Saved plot as {filename}")  # 打印确认消息
        # Show the plot
        plt.show()