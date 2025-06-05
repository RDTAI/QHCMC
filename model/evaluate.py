import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def evaluate_classic(best_G, best_schedule, classic_method):

    print("Final Comprehensive G-score (Method: {}):".format(classic_method), best_G)

    best_schedule_df = pd.DataFrame(best_schedule)
    csv_filename = f'{classic_method}_patient_and_hospital_schedule_{len(best_schedule_df)}comprehensive.csv'
    best_schedule_df.to_csv("results/"+csv_filename, index=False)
    print("Best schedule saved as:", csv_filename)

    delay_times = [entry['Delay Time'] for entry in best_schedule]
    satisfaction_scores = [entry['Satisfaction'] for entry in best_schedule]

    total_delay_time = sum(delay_times)
    total_satisfaction = sum(satisfaction_scores)

    fatigue_scores = {}
    for entry in best_schedule:
        doctor_id = entry['Doctor ID']
        fatigue_duration = entry['Fatigue']
        if doctor_id not in fatigue_scores:
            fatigue_scores[doctor_id] = 0
        fatigue_scores[doctor_id] += fatigue_duration

    total_fatigue = sum(fatigue_scores.values())

    print("Total Delay Time of (Method: {}):".format(classic_method), total_delay_time, 'hours')
    print("Total Satisfaction (Method: {}):".format(classic_method), total_satisfaction, 'points')
    print("Total Fatigue (Method: {}):".format(classic_method), total_fatigue, '(hours)')


def evaluate_ql(env=None, window_size=100, ql_method=None,
                episode_rewards=None, episode_delays=None,
                satisfaction_scores=None, fatigue_scores=None,
                G_score=None, schedule=None,
                num_doctors=None):

    smoothed_rewards = moving_average(episode_rewards, window_size)
    smoothed_delays = moving_average(episode_delays, window_size)
    smoothed_satisfaction = moving_average(satisfaction_scores, window_size)
    smoothed_fatigue = moving_average(fatigue_scores, window_size)
    smoothed_G_score = moving_average(G_score, window_size)


    plt.figure(figsize=(12, 10))  # 调整图形的宽度

    plt.subplot(5, 1, 1)
    plt.plot(smoothed_rewards[1:], label='Smoothed Total Reward', color='orange')
    plt.axhline(y=smoothed_rewards[1], color='red', linestyle='--', linewidth=1)
    plt.axhline(y=smoothed_rewards[-1], color='red', linestyle='--', linewidth=1)
    plt.title(f'Smoothed Total Reward Over Episodes ({ql_method}) ',fontsize=15)
    plt.xlabel('Episode (Smoothed)', fontsize=15)
    plt.ylabel('Total Reward', fontsize=15)
    plt.legend(loc='upper left')

    if smoothed_rewards[-1] > smoothed_rewards[1]:
        plt.annotate('', xy=(len(smoothed_rewards) - 1, smoothed_rewards[-1]),
                     xytext=(len(smoothed_rewards) - 1, smoothed_rewards[1]),
                     arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->',lw=2))
    else:
        plt.annotate('', xy=(len(smoothed_rewards) - 1, smoothed_rewards[-1]),
                     xytext=(len(smoothed_rewards) - 1, smoothed_rewards[1]),
                     arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->',lw=2))


    plt.subplot(5, 1, 2)
    plt.plot(smoothed_delays[1:], label='Smoothed Total Delay',color='purple')
    plt.axhline(y=smoothed_delays[1], color='red', linestyle='--', linewidth=1)
    plt.axhline(y=smoothed_delays[-1], color='red', linestyle='--', linewidth=1)
    plt.title(f'Smoothed Total Delay Over Episodes ({ql_method}) ',fontsize=15)
    plt.xlabel('Episode (Smoothed)', fontsize=15)
    plt.ylabel('Total Delay (Hours)', fontsize=15)
    plt.legend(loc='upper left')

    if smoothed_delays[-1] > smoothed_delays[1]:
        plt.annotate('', xy=(len(smoothed_delays) - 1, smoothed_delays[-1]),
                     xytext=(len(smoothed_delays) - 1, smoothed_delays[1] ),
                     arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->',lw=2))
    else:
        plt.annotate('', xy=(len(smoothed_delays) - 1, smoothed_delays[-1]),
                     xytext=(len(smoothed_delays) - 1, smoothed_delays[1]),
                     arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->',lw=2))

    plt.subplot(5, 1, 3)
    plt.plot((smoothed_satisfaction[1:] / len(schedule)), label='Smoothed Average Satisfaction', color='blue')
    plt.axhline(y=smoothed_satisfaction[1] / len(schedule), color='red', linestyle='--', linewidth=1)
    plt.axhline(y=smoothed_satisfaction[-1] / len(schedule), color='red', linestyle='--', linewidth=1)
    plt.title(
        f'Smoothed Average Satisfaction Over Episodes ({ql_method}) ',fontsize=15)
    plt.xlabel('Episode (Smoothed)', fontsize=15)
    plt.ylabel('Satisfaction (%)', fontsize=15)
    plt.legend(loc='upper left')

    if (smoothed_satisfaction[-1] / len(schedule)) > (smoothed_satisfaction[1] / len(schedule)):
        plt.annotate('', xy=(len(smoothed_satisfaction) - 1, smoothed_satisfaction[-1] / len(schedule)),
                     xytext=(len(smoothed_satisfaction) - 1, (smoothed_satisfaction[1] / len(schedule)) ),
                     arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->',lw=2))
    else:
        plt.annotate('', xy=(len(smoothed_satisfaction) - 1, smoothed_satisfaction[-1] / len(schedule)),
                     xytext=(len(smoothed_satisfaction) - 1, (smoothed_satisfaction[1] / len(schedule)) ),
                     arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->',lw=2))

    plt.subplot(5, 1, 4)
    plt.plot((smoothed_fatigue[1:] / num_doctors), label='Smoothed Average Doctor Fatigue',color='green')
    plt.axhline(y=smoothed_fatigue[1] / num_doctors, color='red', linestyle='--', linewidth=1)
    plt.axhline(y=smoothed_fatigue[-1] / num_doctors, color='red', linestyle='--', linewidth=1)
    plt.title(f'Smoothed Average Fatigue Over Episodes ({ql_method}) ',fontsize=15)
    plt.xlabel('Episode (Smoothed)', fontsize=15)
    plt.ylabel('Fatigue Score', fontsize=15)
    plt.legend(loc='upper left')

    if (smoothed_fatigue[-1] / num_doctors) > (smoothed_fatigue[1] / num_doctors):
        plt.annotate('', xy=(len(smoothed_fatigue) - 1, smoothed_fatigue[-1] / num_doctors),
                     xytext=(len(smoothed_fatigue) - 1, (smoothed_fatigue[1] / num_doctors)),
                     arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->',lw=2))
    else:
        plt.annotate('', xy=(len(smoothed_fatigue) - 1, smoothed_fatigue[-1] / num_doctors),
                     xytext=(len(smoothed_fatigue) - 1, (smoothed_fatigue[1] / num_doctors)),
                     arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->',lw=2))

    plt.subplot(5, 1, 5)
    plt.plot(((smoothed_satisfaction[1:] / len(schedule)) - (smoothed_fatigue[1:] / num_doctors)),
             label='Smoothed Average G Score',color='magenta')
    plt.axhline(y=(smoothed_satisfaction[1] / len(schedule)) - (smoothed_fatigue[1] / num_doctors), color='red',
                linestyle='--', linewidth=1)  # 起点
    plt.axhline(y=(smoothed_satisfaction[-1] / len(schedule)) - (smoothed_fatigue[-1] / num_doctors), color='red',
                linestyle='--', linewidth=1)  # 终点
    plt.title(
        f'Smoothed Average G_score Over Episodes ({ql_method}) ',fontsize=15)
    plt.xlabel('Episode (Smoothed)', fontsize=15)
    plt.ylabel('G Score', fontsize=15)
    plt.legend(loc='upper left')

    if ((smoothed_satisfaction[-1] / len(schedule)) - (smoothed_fatigue[-1] / num_doctors)) > \
            ((smoothed_satisfaction[1] / len(schedule)) - (smoothed_fatigue[1] / num_doctors)):
        plt.annotate('', xy=(len(smoothed_G_score) - 1,
                             (smoothed_satisfaction[-1] / len(schedule)) - (smoothed_fatigue[-1] / num_doctors)),
                     xytext=(len(smoothed_G_score) - 1,
                             ((smoothed_satisfaction[1] / len(schedule)) - (
                                         smoothed_fatigue[1] / num_doctors))),
                     arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->',lw=2))
    else:
        plt.annotate('', xy=(len(smoothed_G_score) - 1,
                             (smoothed_satisfaction[-1] / len(schedule)) - (smoothed_fatigue[-1] / num_doctors)),
                     xytext=(len(smoothed_G_score) - 1,
                             ((smoothed_satisfaction[1] / len(schedule)) - (smoothed_fatigue[1] / num_doctors)) ),
                     arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->',lw=2))

    plt.tight_layout()
    plt.show()

    best_schedule, best_G = env.save_schedule(f'{ql_method}_patient_and_hospital_schedule_{len(schedule)}_{num_doctors}_comprehensive.csv')
    print(f"Best G-score ({ql_method}):", max(smoothed_satisfaction[1:] / len(schedule)) + (smoothed_fatigue[1:] / num_doctors))

    total_satisfaction = sum(item['Satisfaction'] for item in env.best_schedule)
    delay_times = [item['Delay Time'] for item in env.best_schedule]
    total_delay_time = sum(delay_times)

    fatigue_scores_dict = {}
    for entry in best_schedule:
        doctor_id = entry['Doctor ID']
        fatigue_duration = entry['Fatigue']
        if doctor_id not in fatigue_scores_dict:
            fatigue_scores_dict[doctor_id] = 0
        fatigue_scores_dict[doctor_id] += fatigue_duration

    total_fatigue = sum(fatigue_scores_dict.values())

    print(f"Total Delay Time of ({ql_method}):", total_delay_time, 'hours')
    print(f"Total Satisfaction of ({ql_method}):", total_satisfaction, 'points')
    print(f"Total Fatigue Time of Doctors in ({ql_method}):", total_fatigue, 'hours')


def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size), 'valid') / window_size



