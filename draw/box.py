import matplotlib.pyplot as plt
import numpy as np

# 实验数据提取
instances = [13, 14, 15, 16, 17]

# APS 数据
aps_fcfs = [9.66, 9.15, 9.19, 9.22, 9.33]
aps_gao = [9.79, 9.76, 9.79, 9.74, 9.59]
aps_q_learning = [9.91, 9.83, 9.83, 9.82, 9.83]
aps_mchc_q_learning = [9.93, 9.87, 9.84, 9.95, 9.89]

# APF 数据
apf_fcfs = [6.67, 7.89, 7.90, 7.68, 7.07]
apf_gao = [6.04, 6.89, 7.13, 6.57, 6.45]
apf_q_learning = [5.77, 6.99, 7.24, 6.60, 6.29]
apf_mchc_q_learning = [5.65, 6.64, 6.84, 6.54, 6.15]

# APS - APF 数据
aps_apf_fcfs = [aps - apf for aps, apf in zip(aps_fcfs, apf_fcfs)]
aps_apf_gao = [aps - apf for aps, apf in zip(aps_gao, apf_gao)]
aps_apf_q_learning = [aps - apf for aps, apf in zip(aps_q_learning, apf_q_learning)]
aps_apf_mchc_q_learning = [aps - apf for aps, apf in zip(aps_mchc_q_learning, apf_mchc_q_learning)]

# OTSR 数据
otsr_fcfs = [90.6, 77.6, 74.6, 80.5, 80.2]
otsr_gao = [92.9, 90.2, 91.9, 91.4, 87.5]
otsr_q_learning = [94.3, 88.4, 90.2, 95.7, 96.1]
otsr_mchc_q_learning = [94.2, 92.5, 93.1, 97.1, 96.3]

# 创建箱型图的函数
def plot_box_chart(data, labels, ylabel, title):
    plt.figure(figsize=(10, 6))
    plt.boxplot(data, labels=labels)
    plt.title(title, fontsize=20)  # 标题
    plt.xlabel('Methods', fontsize=16)  # 横轴标签
    plt.ylabel(ylabel, fontsize=16)  # 纵轴标签
    plt.xticks(fontsize=14)  # 横轴刻度
    plt.yticks(fontsize=14)  # 纵轴刻度
    plt.grid()
    plt.tight_layout()
    plt.show()

# 绘制不同指标的箱型图
plot_box_chart([aps_fcfs, aps_gao, aps_q_learning, aps_mchc_q_learning],
                ['FCFS', 'GAO', 'Q-Learning', 'MCHC Q-Learning'],
                'APS', 'Box Plot of Algorithms for APS')
plot_box_chart([apf_fcfs, apf_gao, apf_q_learning, apf_mchc_q_learning],
                ['FCFS', 'GAO', 'Q-Learning', 'MCHC Q-Learning'],
                'APF', 'Box Plot of Algorithms for APF')
plot_box_chart([aps_apf_fcfs, aps_apf_gao, aps_apf_q_learning, aps_apf_mchc_q_learning],
                ['FCFS', 'GAO', 'Q-Learning', 'MCHC Q-Learning'],
                'APS - APF', 'Box Plot of Algorithms for APS - APF')
plot_box_chart([otsr_fcfs, otsr_gao, otsr_q_learning, otsr_mchc_q_learning],
               ['FCFS', 'GAO', 'Q-Learning', 'MCHC Q-Learning'],
               'OTSR (%)', 'Box Plot of Algorithms for OTSR (%)')