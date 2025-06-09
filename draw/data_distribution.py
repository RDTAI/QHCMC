import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('../dataset/base_patients_surgery_224_schedule.csv')
# Convert 'Start Time' to datetime objects for easier manipulation
df['Start Time'] = pd.to_datetime(df['Start Time'], format='%H:%M')
import matplotlib.pyplot as plt
import seaborn as sns

# # 图1：Surgery Duration Distribution
# plt.figure(figsize=(8, 6))
# sns.histplot(df['Duration (hours)'], kde=True, color="#71CEEF")
# plt.title('Distribution of Surgery Duration')
# plt.xlabel('Duration (hours)')
# plt.ylabel('Proportion of Patients')
# plt.show()

# 图2：Day of Week Distribution
plt.figure(figsize=(12, 10))
sns.countplot(x='Day', data=df, order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], color="#9370DB")
plt.title('Distribution of Surgeries Across Days of the Week',fontsize=16)
plt.xlabel('Day of the Week',fontsize=16)
plt.ylabel('Number of Surgeries',fontsize=16)
plt.xticks(rotation=45, ha="right",fontsize=16)
plt.ylim(0, max(df['Day'].value_counts()) + 5)
plt.show()

# 图3：Surgery Type Distribution
plt.figure(figsize=(20, 12))
sns.countplot(y='Surgery Type', data=df, color="#BA55D3")
plt.title('Distribution of Surgery Types',fontsize=20)
plt.xlabel('Number of Patients',fontsize=20)
plt.ylabel('Surgery Type',fontsize=20)
plt.yticks(rotation=65, ha="right", fontsize=16)
plt.xlim(0, max(df['Surgery Type'].value_counts()) + 5)
plt.show()

# # 图4：Emergency Status Distribution
# plt.figure(figsize=(8, 6))
# sns.countplot(x='Emergency', data=df, color="#87CEEB", width=0.4)
# plt.title('Proportion of Emergency Surgeries')
# plt.xlabel('Emergency Status')
# plt.ylabel('Proportion of Patients')
# plt.show()
# #
# # Create subplots
# fig, axes = plt.subplots(2, 2, figsize=(15, 10))
# color_palette = "#A3C1DA"
# # Plot 1: Surgery Duration Distribution
# sns.histplot(df['Duration (hours)'], ax=axes[0, 0], kde=True, color="#71CEEF") #Added color
# axes[0, 0].set_title('Distribution of Surgery Duration')
# axes[0, 0].set_xlabel('Duration (hours)')
# axes[0, 0].set_ylabel('Proportion of Patients')
#
#
# # Plot 2: Day of Week Distribution
# sns.countplot(x='Day', data=df, ax=axes[0, 1], order= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], color="#87CEEB") #Added color
# axes[0, 1].set_title('Distribution of Surgeries Across Days of the Week')
# axes[0, 1].set_xlabel('Day of the Week')
# axes[0, 1].set_ylabel('Proportion of Patients')
# axes[0,1].set_xticklabels(axes[0,1].get_xticklabels(), rotation=45, ha="right")
# axes[0,1].set_ylim(0,max(df['Day'].value_counts())+5)
#
#
# # Plot 3: Surgery Type Distribution
# sns.countplot(y='Surgery Type', data=df, ax=axes[1, 0], color="#87CEEB")
# axes[1, 0].set_title('Distribution of Surgery Types')
# axes[1, 0].set_xlabel('Proportion of Patients')
# axes[1, 0].set_ylabel('Surgery Type')
# axes[1, 0].set_yticklabels(axes[1, 0].get_yticklabels(), rotation=65, ha="right", fontsize=5) # fontsize=8 reduces font size
# axes[1, 0].set_xlim(0, max(df['Surgery Type'].value_counts()) + 5)
#
# # Plot 4: Emergency Status Distribution
# sns.countplot(x='Emergency', data=df, ax=axes[1, 1], color="#87CEEB", width=0.4) #Added color and reduced width
# axes[1, 1].set_title('Proportion of Emergency Surgeries')
# axes[1, 1].set_xlabel('Emergency Status')
# axes[1, 1].set_ylabel('Proportion of Patients')
#
# # Adjust layout and display the plots
# plt.tight_layout()
# plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import numpy as np

# Load the data
df = pd.read_csv('../results/base_patients_surgery_schedule.csv')

# Convert 'Start Time' to datetime objects for easier manipulation
df['Start Time'] = pd.to_datetime(df['Start Time'], format='%H:%M')
#
# # Set up the figure
plt.figure(figsize=(15, 10))

# Plot 1: KDE for Surgery Duration Distribution
plt.subplot(2, 1, 1)
sns.kdeplot(df['Duration (hours)'], fill=True, color='blue', alpha=0.5)
plt.title('KDE of Surgery Duration', fontsize=20)
plt.xlabel('Duration (hours)', fontsize=20)
plt.ylabel('Density', fontsize=20)

# Plot 2: Clustering Analysis for Surgery Types
# Prepare the data for clustering
type_counts = df['Surgery Type'].value_counts().reset_index()
type_counts.columns = ['Surgery Type', 'Count']

# Reshape data for clustering
data_for_clustering = type_counts[['Count']].values

# Apply KMeans
kmeans = KMeans(n_clusters=3)  # Choose number of clusters
type_counts['Cluster'] = kmeans.fit_predict(data_for_clustering)

# Create scatter plot for clusters
plt.subplot(2, 1, 2)
sns.scatterplot(data=type_counts, x='Surgery Type', y='Count', hue='Cluster', palette='deep', s=100)
plt.title('Surgery Type Count Clustering', fontsize=20)
plt.xlabel('Surgery Type', fontsize=20)
plt.ylabel('Count', fontsize=20)
plt.xticks(rotation=20)

# Adjust layout
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.cluster import KMeans

# 假设 hospital_data 变量已经定义并包含医院与手术类型的信息
# 这里正在构建 DataFrame 来适合进行可视化
data = {
    'Surgery Type': [],
    'Count': []
}

hospital_data = {
        'H01': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(1, 10)],  # OR01..OR04
            'doctors': {
                'General Surgery': ['D01', 'D23'],
                'Obstetrics and Gynecology Surgery': ['D02', 'D24', 'D42'],
                'Otorhinolaryngology Surgery': ['D03', 'D25'],
                'Ophthalmic Surgery': ['D04', 'D26'],
                'Urologic Surgery': ['D05', 'D27'],
                'Gastrointestinal Surgery': ['D06', 'D28']
            }
        },
        'H02': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(10, 20)],  # OR05..OR09
            'doctors': {
                'General Surgery': ['D07', 'D29'],
                'Obstetrics and Gynecology Surgery': ['D08', 'D30', 'D43'],
                'Otorhinolaryngology Surgery': ['D09', 'D13', 'D31'],
                'Ophthalmic Surgery': ['D10', 'D14', 'D32'],
                'Urologic Surgery': ['D11', 'D33'],
                'Gastrointestinal Surgery': ['D12', 'D34']
            }
        },
        'H03': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(20, 30)],  # OR10..OR16
            'doctors': {
                'General Surgery': ['D15', 'D35', 'D36'],
                'Obstetrics and Gynecology Surgery': ['D16', 'D37'],
                'Otorhinolaryngology Surgery': ['D17', 'D38'],
                'Ophthalmic Surgery': ['D18', 'D39', 'D44'],
                'Urologic Surgery': ['D19', 'D21', 'D40'],
                'Gastrointestinal Surgery': ['D20', 'D22', 'D41']
            }
        },
        'H04': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(30, 40)],  # OR10..OR16
            'doctors': {
                'General Surgery': ['D45', 'D46', 'D47'],
                'Obstetrics and Gynecology Surgery': ['D48', 'D49', 'D50'],
                'Otorhinolaryngology Surgery': ['D51', 'D52'],
                'Ophthalmic Surgery': ['D53', 'D54'],
                'Urologic Surgery': ['D55', 'D56', 'D57'],
                'Gastrointestinal Surgery': ['D58', 'D59', 'D60']
            }
        },
        'H05': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(40, 50)],  # OR10..OR16
            'doctors': {
                'General Surgery': ['D61', 'D62', 'D63'],
                'Obstetrics and Gynecology Surgery': ['D64', 'D65', 'D66'],
                'Otorhinolaryngology Surgery': ['D67', 'D68', 'D76'],
                'Ophthalmic Surgery': ['D69', 'D70'],
                'Urologic Surgery': ['D71', 'D72', 'D73'],
                'Gastrointestinal Surgery': ['D74', 'D75']
            }
        },
        'H06': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(50, 60)],  # OR10..OR16
            'doctors': {
                'General Surgery': ['D77', 'D78'],
                'Obstetrics and Gynecology Surgery': ['D80', 'D81', 'D82'],
                'Otorhinolaryngology Surgery': ['D83', 'D84'],
                'Ophthalmic Surgery': ['D85', 'D86', 'D79'],
                'Urologic Surgery': ['D87', 'D88', 'D89'],
                'Gastrointestinal Surgery': ['D90', 'D91', 'D92']
            }
        },
        'H07': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(60, 70)],  # OR10..OR16
            'doctors': {
                'General Surgery': ['D93', 'D94', 'D95'],
                'Obstetrics and Gynecology Surgery': ['D96', 'D97', 'D98'],
                'Otorhinolaryngology Surgery': ['D99', 'D100'],
                'Ophthalmic Surgery': ['D101', 'D102'],
                'Urologic Surgery': ['D103', 'D104', 'D105'],
                'Gastrointestinal Surgery': ['D106', 'D107', 'D108']
            }
        },
        'H08': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(70, 80)],  # OR10..OR16
            'doctors': {
                'General Surgery': ['D109', 'D110', 'D112'],
                'Obstetrics and Gynecology Surgery': ['D113', 'D114'],
                'Otorhinolaryngology Surgery': ['D116', 'D117', 'D115'],
                'Ophthalmic Surgery': ['D118', 'D119', 'D128'],
                'Urologic Surgery': ['D120', 'D121', 'D122'],
                'Gastrointestinal Surgery': ['D123', 'D124', 'D125']
            }
        },
        'H09': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(80, 90)],  # OR10..OR16
            'doctors': {
                'General Surgery': ['D126', 'D127'],
                'Obstetrics and Gynecology Surgery': ['D129', 'D130'],
                'Otorhinolaryngology Surgery': ['D132', 'D133', 'D131'],
                'Ophthalmic Surgery': ['D134', 'D135', 'D138'],
                'Urologic Surgery': ['D136', 'D137'],
                'Gastrointestinal Surgery': ['D139', 'D140', 'D141']
            }
        },
        'H10': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(90, 100)],  # OR10..OR16
            'doctors': {
                'General Surgery': ['D142', 'D143', 'D144'],
                'Obstetrics and Gynecology Surgery': ['D145', 'D146', 'D147'],
                'Otorhinolaryngology Surgery': ['D148', 'D149', 'D150'],
                'Ophthalmic Surgery': ['D151', 'D152', 'D153'],
                'Urologic Surgery': ['D154', 'D155', 'D156'],
                'Gastrointestinal Surgery': ['D157', 'D158', 'D159']
            }
        },
        'H11': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(100, 110)],  # OR10..OR16
            'doctors': {
                'General Surgery': ['D160', 'D161', 'D162'],
                'Obstetrics and Gynecology Surgery': ['D163', 'D164'],
                'Otorhinolaryngology Surgery': ['D165', 'D166', 'D167'],
                'Ophthalmic Surgery': ['D168', 'D169', 'D170'],
                'Urologic Surgery': ['D171', 'D172', 'D173'],
                'Gastrointestinal Surgery': ['D174', 'D175', 'D176']
            }
        },
        'H12': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(110, 120)],  # OR10..OR16
            'doctors': {
                'General Surgery': ['D177', 'D178', 'D179'],
                'Obstetrics and Gynecology Surgery': ['D180', 'D181', 'D182'],
                'Otorhinolaryngology Surgery': ['D183', 'D184', 'D185'],
                'Ophthalmic Surgery': ['D186', 'D187', 'D188'],
                'Urologic Surgery': ['D189', 'D190', 'D191'],
                'Gastrointestinal Surgery': ['D192', 'D193', 'D194']
            }
        },
        'H13': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(120, 130)],  # OR10..OR16
            'doctors': {
                'General Surgery': ['D126', 'D127'],
                'Obstetrics and Gynecology Surgery': ['D129', 'D130'],
                'Otorhinolaryngology Surgery': ['D132', 'D133', 'D131'],
                'Ophthalmic Surgery': ['D134', 'D135', 'D138'],
                'Urologic Surgery': ['D136', 'D137'],
                'Gastrointestinal Surgery': ['D139', 'D140', 'D141']
            }
        }
    }
# 填充数据
for hospital_id, hospital_info in hospital_data.items():
    print(f"Processing {hospital_id}: {hospital_info}")  # 打印医院信息
    for surgery_type, doctors in hospital_info['doctors'].items():
        print(f"  Surgery Type: {surgery_type}, Doctors: {doctors}")  # 打印手术类型及医生成员
        data['Surgery Type'].append(surgery_type)
        data['Count'].append(len(doctors))

# 转换为 DataFrame
df = pd.DataFrame(data)

# Set up the figure
plt.figure(figsize=(15, 10))

# Plot 1: KDE for Surgery Type Count Distribution
plt.subplot(2, 1, 1)
sns.kdeplot(df['Count'], fill=True, color='blue', alpha=0.5)
plt.title('KDE of Surgery Type Count', fontsize=16)
plt.xlabel('Count', fontsize=14)
plt.ylabel('Density', fontsize=14)

# Plot 2: Clustering Analysis for Surgery Types
# Prepare the data for clustering
type_counts = df['Surgery Type'].value_counts().reset_index()
type_counts.columns = ['Surgery Type', 'Count']

# Reshape data for clustering
data_for_clustering = type_counts[['Count']].values

# Apply KMeans
kmeans = KMeans(n_clusters=6)  # Choose number of clusters
type_counts['Cluster'] = kmeans.fit_predict(data_for_clustering)

# Create scatter plot for clusters
plt.subplot(2, 1, 2)
sns.scatterplot(data=type_counts, x='Surgery Type', y='Count', hue='Cluster', palette='deep', s=100)
plt.title('Surgery Type Count Clustering', fontsize=16)
plt.xlabel('Surgery Type', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.xticks(rotation=45)

# Adjust layout
plt.tight_layout()
plt.show()


# 使用多种紫色系颜色绘制图表
colors = ['#EE82EE', '#9370DB', '#BA55D3', '#9400D3', '#D8BFD8']

plt.figure(figsize=(8, 3))
for i, color in enumerate(colors):
    plt.fill_between([i, i+1], 0, 1, color=color)

plt.xlim(0, len(colors))
plt.axis('off')
plt.show()