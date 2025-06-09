import pandas as pd

from model.QL import QLearningAgent, SurgerySchedulingEnv, train_agent_ql
from model.classic import  GeneticAlgorithmScheduler
from model.evaluate import evaluate_classic, evaluate_ql

def calculate_metrics(file_path, num_doctors, schedule_df, percentiles):

    df = pd.read_csv(file_path)
    for percentile in percentiles:
        num_rows = int(len(schedule_df) * percentile)
        subset_df = df.iloc[:num_rows]

        TPD = subset_df['Delay Time'].sum()
        APD = TPD / len(subset_df)
        TPS = subset_df['Satisfaction'].sum()
        APS = TPS / len(subset_df)
        TPF = subset_df['Fatigue'].sum()
        APF = TPF / num_doctors
        TPS_minus_TPF = TPS - TPF
        APS_minus_APF = APS - APF
        on_time_cases = subset_df[(subset_df['Delay Time'] == 0)]
        OTSR = len(on_time_cases) / len(subset_df)
        OTR = 1 - OTSR

        print(f"Metrics for {file_path} at {percentile * 100}%:")
        print(f"Total Patient Delay (TPD): {TPD}")
        print(f"Average Patient Delay (APD): {APD}")
        print(f"Total Patient Satisfaction (TPS): {TPS}")
        print(f"Average Patient Satisfaction (APS): {APS}")
        print(f"Total Physician Fatigue (TPF): {TPF}")
        print(f"Average Physician Fatigue (APF): {APF}")
        print(f"TPS - TPF: {TPS_minus_TPF}")
        print(f"APS - APF: {APS_minus_APF}")
        print(f"On Time Surgery Rate (OTSR): {OTSR * 100}%")
        print(f"Overtime Rate (OTR): {OTR * 100}%")

def main():
    num_patient = 40
    schedule_df = pd.read_csv(f'dataset/base_patients_surgery_{num_patient}_schedule.csv')
    hospital_data = {
        'H01': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(1, 10)],
            'doctors': {
                'General Surgery': ['D01', 'D23'],
                'Obstetrics and Gynecology Surgery': ['D02', 'D24'],
                'Otorhinolaryngology Surgery': ['D03','D25'],
                'Ophthalmic Surgery': ['D04', 'D26'],
                'Urologic Surgery': ['D05', 'D27'],
                'Gastrointestinal Surgery': ['D06', 'D28']
            }
        },
        # 'H02': {
        #     'rooms': [f'OR{str(i).zfill(2)}' for i in range(10, 20)],
        #     'doctors': {
        #         'General Surgery': ['D07','D31', 'D13'],
        #         'Obstetrics and Gynecology Surgery': ['D08', 'D30'],
        #         'Otorhinolaryngology Surgery': ['D09', 'D33', 'D34'],
        #         'Ophthalmic Surgery': ['D10', 'D14','D42'],
        #         'Urologic Surgery': ['D11', 'D32','D29'],
        #         'Gastrointestinal Surgery': ['D12', 'D43']
        #     }
        # },
        'H03': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(20, 30)],
            'doctors': {
                'General Surgery': ['D15','D40', 'D37',],
                'Obstetrics and Gynecology Surgery': ['D16', 'D22', 'D41'],
                'Otorhinolaryngology Surgery': ['D17', 'D35'],
                'Ophthalmic Surgery': ['D18','D38'],
                'Urologic Surgery': ['D19', 'D21', 'D36'],
                'Gastrointestinal Surgery': ['D20','D44', 'D39',]
            }
        },
        # 'H04': {
        #     'rooms': [f'OR{str(i).zfill(2)}' for i in range(30, 40)],
        #     'doctors': {
        #         'General Surgery': ['D45'],
        #         'Obstetrics and Gynecology Surgery': ['D48'],
        #         'Otorhinolaryngology Surgery': ['D51'],
        #         'Ophthalmic Surgery': ['D53', 'D54', 'D66'],
        #         'Urologic Surgery': ['D55', 'D56', 'D57', 'D59', 'D60', 'D46', 'D47', 'D49', 'D50', 'D52', 'D63'],
        #         'Gastrointestinal Surgery': ['D58']
        #     }
        # },
        # 'H05': {
        #     'rooms': [f'OR{str(i).zfill(2)}' for i in range(40, 50)],  # OR10..OR16
        #     'doctors': {
        #         'General Surgery': ['D61'],
        #         'Obstetrics and Gynecology Surgery': ['D64', 'D66'],
        #         'Otorhinolaryngology Surgery': ['D67'],
        #         'Ophthalmic Surgery': ['D69'],
        #         'Urologic Surgery': ['D71', 'D72', 'D73', 'D75', 'D76', 'D70',  'D65'],
        #         'Gastrointestinal Surgery': ['D74']
        #     }
        # },
        # 'H06': {
        #     'rooms': [f'OR{str(i).zfill(2)}' for i in range(50, 60)],  # OR10..OR16
        #     'doctors': {
        #         'General Surgery': ['D77', 'D78'],
        #         'Obstetrics and Gynecology Surgery': ['D80', 'D81'],
        #         'Otorhinolaryngology Surgery': ['D83', 'D84', 'D82'],
        #         'Ophthalmic Surgery': ['D85', 'D86', 'D92', 'D99'],
        #         'Urologic Surgery': ['D87', 'D88', 'D89'],
        #         'Gastrointestinal Surgery': ['D90', 'D91', 'D79']
        #     }
        # }
    }
    hospital_data_ql_mh = {
        'H01': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(1, 10)],
            'doctors': {
                'General Surgery': ['D01', 'D23'],
                'Obstetrics and Gynecology Surgery': ['D02', 'D24'],
                'Otorhinolaryngology Surgery': ['D03', 'D25'],
                'Ophthalmic Surgery': ['D04', 'D26'],
                'Urologic Surgery': ['D05', 'D27'],
                'Gastrointestinal Surgery': ['D06', 'D28']
            }
        },
        'H02': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(10, 20)],
            'doctors': {
                'General Surgery': ['D07'],
                'Obstetrics and Gynecology Surgery': ['D08'],
                'Otorhinolaryngology Surgery': ['D09'],
                'Ophthalmic Surgery': ['D10'],
                'Urologic Surgery': ['D11'],
                'Gastrointestinal Surgery': ['D12']
            }
        },
        # 'H02': {
        #     'rooms': [f'OR{str(i).zfill(2)}' for i in range(10, 20)],
        #     'doctors': {
        #         'General Surgery': ['D07', 'D31', 'D13'],
        #         'Obstetrics and Gynecology Surgery': ['D08', 'D30'],
        #         'Otorhinolaryngology Surgery': ['D09', 'D33', 'D34'],
        #         'Ophthalmic Surgery': ['D10', 'D14', 'D42'],
        #         'Urologic Surgery': ['D11', 'D32', 'D29'],
        #         'Gastrointestinal Surgery': ['D12', 'D43']
        #     }
        # },
        # 'H03': {
        #     'rooms': [f'OR{str(i).zfill(2)}' for i in range(20, 30)],
        #     'doctors': {
        #         'General Surgery': ['D15', 'D40', 'D37', ],
        #         'Obstetrics and Gynecology Surgery': ['D16', 'D22', 'D41'],
        #         'Otorhinolaryngology Surgery': ['D17', 'D35'],
        #         'Ophthalmic Surgery': ['D18', 'D38'],
        #         'Urologic Surgery': ['D19', 'D21', 'D36'],
        #         'Gastrointestinal Surgery': ['D20', 'D44', 'D39', ]
        #     }
        # },
        # 'H04': {
        #     'rooms': [f'OR{str(i).zfill(2)}' for i in range(30, 40)],
        #     'doctors': {
        #         'General Surgery': ['D45', 'D52', 'D63'],
        #         'Obstetrics and Gynecology Surgery': ['D48', 'D49', 'D50'],
        #         'Otorhinolaryngology Surgery': ['D51', 'D46', 'D47'],
        #         'Ophthalmic Surgery': ['D53', 'D54', 'D66'],
        #         'Urologic Surgery': ['D55', 'D56', 'D57'],
        #         'Gastrointestinal Surgery': ['D58', 'D59', 'D60']
        #     }
        # },
        # 'H05': {
        #     'rooms': [f'OR{str(i).zfill(2)}' for i in range(40, 50)],
        #     'doctors': {
        #         'General Surgery': ['D61'],
        #         'Obstetrics and Gynecology Surgery': ['D64', 'D66'],
        #         'Otorhinolaryngology Surgery': ['D67'],
        #         'Ophthalmic Surgery': ['D69'],
        #         'Urologic Surgery': ['D71', 'D72', 'D73', 'D75', 'D76', 'D70',  'D65'],
        #         'Gastrointestinal Surgery': ['D74']
        #     }
        # },
        'H06': {
            'rooms': [f'OR{str(i).zfill(2)}' for i in range(50, 60)],
            'doctors': {
                'General Surgery': ['D77', 'D78'],
                'Obstetrics and Gynecology Surgery': ['D80', 'D81'],
                'Otorhinolaryngology Surgery': ['D83', 'D84', 'D82'],
                'Ophthalmic Surgery': ['D85', 'D86'],
                'Urologic Surgery': ['D87', 'D88'],
                'Gastrointestinal Surgery': ['D90', 'D91']
            }
        }
    }

    total_doctors_ql = 0
    for hospital in hospital_data.values():
        for doctor_list in hospital['doctors'].values():
            total_doctors_ql += len(doctor_list)
    print("Total doctors for QL: ", total_doctors_ql)
    total_doctors_ql_mh = 0
    for hospital in hospital_data_ql_mh.values():
        for doctor_list in hospital['doctors'].values():
            total_doctors_ql_mh += len(doctor_list)
    print("Total doctors for QL MH: ", total_doctors_ql_mh)
    a = 1
    b = 1

    gao = GeneticAlgorithmScheduler(hospitals=hospital_data, schedule_df=schedule_df, population_size=500,generations=50, mutation_rate=0.05,a=a, b=b)
    best_schedule_gao, best_G_gao = gao.optimize()
    evaluate_classic(best_G_gao, best_schedule_gao, classic_method='gao')

    env = SurgerySchedulingEnv(hospitals=hospital_data, schedule_df=schedule_df,a=a, b=b)
    action_mapping = env.create_action_mapping()
    state_size = len(schedule_df)
    agent_ql = QLearningAgent(state_size, len(action_mapping), action_mapping)

    # Run Q-Learning MH methods
    # env_mh = SurgerySchedulingEnvMH(hospitals=hospital_data_ql_mh, schedule_df=schedule_df, a=a, b=b)
    # action_mapping = env_mh.create_action_mapping()  # Create the action mapping. This should be implemented in SurgerySchedulingEnv
    # state_size = len(schedule_df)
    # agent_ql_mh = QLearningAgentMH(state_size, len(action_mapping), action_mapping)

    episode_rewards_ql, satisfaction_scores_ql, fatigue_scores_ql, G_score_ql, episode_delays_ql = train_agent_ql(
        agent_ql, env , schedule_df=schedule_df, episodes=1100,a=a,b=b)

    # episode_rewards_ql_mh, satisfaction_scores_ql_mh, fatigue_scores_ql_mh, G_score_ql_mh, episode_delays_ql_mh = train_agent_ql(
    #     agent_ql_mh, env_mh, schedule_df=schedule_df, episodes=1100, a=a, b=b)
    print(f"QL agent training complete. Rewards : {episode_rewards_ql}; Satisfaction: {satisfaction_scores_ql}; Fatigue: {fatigue_scores_ql}; G_score: {G_score_ql}; Delays: {episode_delays_ql}")
    # print(f"QL MH agent training complete. Rewards : {episode_rewards_ql_mh}; Satisfaction: {satisfaction_scores_ql_mh}; Fatigue: {fatigue_scores_ql_mh}; G_score: {G_score_ql_mh}; Delays: {episode_delays_ql_mh}")
    #
    evaluate_ql(env=env, window_size=100, ql_method='Q-Learning',
                episode_rewards=episode_rewards_ql, episode_delays=episode_delays_ql,
                satisfaction_scores=satisfaction_scores_ql, fatigue_scores=fatigue_scores_ql,
                G_score=G_score_ql, schedule=schedule_df,
                num_doctors=total_doctors_ql)
    # evaluate_ql(env=env, window_size=100, ql_method='HCMC Q-Learning',
    #             episode_rewards=episode_rewards_ql_mh, episode_delays=episode_delays_ql_mh,
    #             satisfaction_scores=satisfaction_scores_ql_mh, fatigue_scores=fatigue_scores_ql_mh,
    #             G_score=G_score_ql_mh, schedule=schedule_df,
    #             num_doctors=total_doctors_ql_mh, num_patients=len(schedule_df))

    # classic_methods = ['gao','Q-Learning','HCMC Q-Learning']
    # for method in classic_methods:
    #        file_path = f'results/{method}_patient_and_hospital_schedule_comprehensive.csv'
    #        calculate_metrics(file_path, total_doctors_ql,schedule_df,percentiles=[1])

if __name__ == '__main__':
    main()
