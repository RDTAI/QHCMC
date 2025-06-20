import argparse
import pandas as pd
import logging
import pandas as pd

from model.QL import QLearningAgent, SurgerySchedulingEnv, train_agent_ql, SurgerySchedulingEnvMH, QLearningAgentMH
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


def main(args):

    schedule_df = pd.read_csv(
        args.schedule_csv if args.schedule_csv else f'dataset/base_patients_surgery_{args.num_patients}_schedule.csv'
    )

    hospital_data = {}
    for i in range(1, args.num_hospitals + 1):
        hospital_id = f"H{str(i).zfill(2)}"
        hospital_data[hospital_id] = {
            'rooms': [f'OR{str(j).zfill(2)}' for j in range(1, 10 if i == 1 else 20)],
            'doctors': {
                'General Surgery': [f'D{str(i * 10 + 1).zfill(2)}', f'D{str(i * 10 + 23).zfill(2)}'],
                'Obstetrics and Gynecology Surgery': [f'D{str(i * 10 + 2).zfill(2)}', f'D{str(i * 10 + 24).zfill(2)}'],
                'Otorhinolaryngology Surgery': [f'D{str(i * 10 + 3).zfill(2)}', f'D{str(i * 10 + 25).zfill(2)}'],
                'Ophthalmic Surgery': [f'D{str(i * 10 + 4).zfill(2)}', f'D{str(i * 10 + 26).zfill(2)}'],
                'Urologic Surgery': [f'D{str(i * 10 + 5).zfill(2)}', f'D{str(i * 10 + 27).zfill(2)}'],
                'Gastrointestinal Surgery': [f'D{str(i * 10 + 6).zfill(2)}', f'D{str(i * 10 + 28).zfill(2)}']
            }
        }
    if args.method == 'GAO':

        logging.info("Running Genetic Algorithm Optimization (GAO)...")

        gao = GeneticAlgorithmScheduler(hospitals = hospital_data, schedule_df = schedule_df, population_size = 500,
                                        generations = 50, mutation_rate = 0.05, a = args.a, b = args.b)
        best_schedule_gao, best_G_gao = gao.optimize()
        evaluate_classic(best_G_gao, best_schedule_gao, classic_method='gao')
    elif args.method == 'QL':

        logging.info("Running Q-Learning...")
        total_doctors_ql = sum(len(hospital['doctors']) for hospital in hospital_data.values())

        env = SurgerySchedulingEnv(hospitals=hospital_data, schedule_df=schedule_df, a = args.a, b = args.b)
        action_mapping = env.create_action_mapping()
        state_size = len(schedule_df)
        agent_ql = QLearningAgent(state_size, len(action_mapping), action_mapping)

        episode_rewards_ql, satisfaction_scores_ql, fatigue_scores_ql, G_score_ql, episode_delays_ql = train_agent_ql(
            agent_ql, env, schedule_df=schedule_df, episodes=1100, a = args.a, b = args.b)
        print(
            f"QL agent training complete. Rewards : {episode_rewards_ql}; Satisfaction: {satisfaction_scores_ql}; Fatigue: {fatigue_scores_ql}; G_score: {G_score_ql}; Delays: {episode_delays_ql}")
        evaluate_ql(env=env, window_size=100, ql_method='Q-Learning',
                episode_rewards=episode_rewards_ql, episode_delays=episode_delays_ql,
                satisfaction_scores=satisfaction_scores_ql, fatigue_scores=fatigue_scores_ql,
                G_score=G_score_ql, schedule=schedule_df,
                num_doctors=total_doctors_ql)
    elif args.method == 'HCMC QL':

        logging.info("Running HCMC Q-Learning...")
        total_doctors_ql_mh = sum(len(hospital['doctors']) for hospital in hospital_data.values())

        env_mh = SurgerySchedulingEnvMH(hospitals=hospital_data, schedule_df=schedule_df, a = args.a, b = args.b)
        action_mapping = env_mh.create_action_mapping()  # Create the action mapping. This should be implemented in SurgerySchedulingEnv
        state_size = len(schedule_df)
        agent_ql_mh = QLearningAgentMH(state_size, len(action_mapping), action_mapping)

        episode_rewards_ql_mh, satisfaction_scores_ql_mh, fatigue_scores_ql_mh, G_score_ql_mh, episode_delays_ql_mh = train_agent_ql(
            agent_ql_mh, env_mh, schedule_df=schedule_df, episodes=1100,a = args.a, b = args.b)
        print(
            f"QL MH agent training complete. Rewards : {episode_rewards_ql_mh}; Satisfaction: {satisfaction_scores_ql_mh}; Fatigue: {fatigue_scores_ql_mh}; G_score: {G_score_ql_mh}; Delays: {episode_delays_ql_mh}")

        evaluate_ql(env=env_mh, window_size=100, ql_method='HCMC Q-Learning',
                    episode_rewards=episode_rewards_ql_mh, episode_delays=episode_delays_ql_mh,
                    satisfaction_scores=satisfaction_scores_ql_mh, fatigue_scores=fatigue_scores_ql_mh,
                    G_score=G_score_ql_mh, schedule=schedule_df,
                    num_doctors=total_doctors_ql_mh)

    # classic_methods = ['gao','Q-Learning','HCMC Q-Learning']
    # for method in classic_methods:
    #        file_path = f'results/{method}_patient_and_hospital_schedule_comprehensive.csv'
    #        calculate_metrics(file_path, total_doctors_ql,schedule_df,percentiles=[1])


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description='Hospital scheduling parameters')
    parser.add_argument(
        '--num_hospitals',
        type=int,
        default=2,
        help='Number of hospitals')
    parser.add_argument(
        '--num_patients',
        type=int,
        default=40,
        help='Number of patients')
    parser.add_argument(
        '--schedule_csv',
        type=str,
        default=None,
        help='Path to schedule CSV file. Defaults to generated path if not provided.')
    parser.add_argument(
        '--a',
        type=float,
        default=1.0,
        help='Weight for patient satisfaction')
    parser.add_argument(
        '--b',
        type=float,
        default=1.0,
        help='Weight for doctor fatigue')
    parser.add_argument(
        '--method',
        type=str,
        default='QL',
        choices=["QL", "HCMC QL", "GAO"],)


    args = parser.parse_args()

    main(args)