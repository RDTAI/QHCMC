import matplotlib.pyplot as plt

# 实验数据提取
instances = [13, 14, 15, 16, 17]

# 换成instances = [15, 14, 16, 17, 13]
# APS 数据
aps_fcfs = [ 9.19,9.15,  9.22, 9.33, 9.66]
aps_gao = [ 9.79, 9.76, 9.74, 9.59,9.79]
aps_q_learning = [ 9.83, 9.83, 9.82, 9.83,9.91]
aps_mchc_q_learning = [9.84,  9.87, 9.95, 9.89,9.93]

# APF 数据
apf_fcfs = [ 7.90,7.89, 7.68, 7.07,6.67]
apf_gao = [ 7.13, 6.89,6.57, 6.45,6.04]
apf_q_learning = [7.24,6.99,  6.60, 6.29,5.77]
apf_mchc_q_learning = [6.84,6.64,  6.54, 6.15,5.65]

# APS - APF 数据
aps_apf_fcfs = [aps - apf for aps, apf in zip(aps_fcfs, apf_fcfs)]
aps_apf_gao = [aps - apf for aps, apf in zip(aps_gao, apf_gao)]
aps_apf_q_learning = [aps - apf for aps, apf in zip(aps_q_learning, apf_q_learning)]
aps_apf_mchc_q_learning = [aps - apf for aps, apf in zip(aps_mchc_q_learning, apf_mchc_q_learning)]

# OTSR 数据
otsr_fcfs = [ 74.6, 77.6,80.5, 80.2,90.6]
otsr_gao = [ 91.9,90.2, 91.4, 87.5,92.9]
otsr_q_learning = [90.2, 88.4, 95.7, 96.1,94.3]
otsr_mchc_q_learning = [ 93.1, 92.5,97.1, 96.3,94.2]

# 创建折线图的函数
def plot_line_chart(x, y_data, labels, ylabel, title):
    plt.figure(figsize=(10, 6))
    for y, label in zip(y_data, labels):
        plt.plot(x, y, marker='o', label=label)
    plt.title(title, fontsize=20)  # 增加标题字体大小
    plt.xlabel('Instances', fontsize=20)  # 增加横轴标签字体大小
    plt.ylabel(ylabel, fontsize=20)  # 增加纵轴标签字体大小
    plt.xticks(x, fontsize=20)  # 增加横轴刻度字体大小
    plt.yticks(fontsize=20)  # 增加纵轴刻度字体大小
    plt.legend(fontsize=20, loc='upper left')  # 图例放在右上角并调整字体大小
    plt.grid()
    plt.tight_layout()
    plt.show()

# 绘制不同指标的折线图
plot_line_chart(instances, [aps_fcfs, aps_gao, aps_q_learning, aps_mchc_q_learning],
                ['FCFS', 'GAO', 'Q-Learning', 'MCHC Q-Learning'],
                'APS', 'Comparison of Algorithms for APS')
plot_line_chart(instances, [apf_fcfs, apf_gao, apf_q_learning, apf_mchc_q_learning],
                ['FCFS', 'GAO', 'Q-Learning', 'MCHC Q-Learning'],
                'APF', 'Comparison of Algorithms for APF')
plot_line_chart(instances, [aps_apf_fcfs, aps_apf_gao, aps_apf_q_learning, aps_apf_mchc_q_learning],
                ['FCFS', 'GAO', 'Q-Learning', 'MCHC Q-Learning'],
                'APS - APF', 'Comparison of Algorithms for APS - APF')
plot_line_chart(instances, [otsr_fcfs, otsr_gao, otsr_q_learning, otsr_mchc_q_learning],
                ['FCFS', 'GAO', 'Q-Learning', 'MCHC Q-Learning'],
                'OTSR (%)', 'Comparison of Algorithms for OTSR (%)')