import pandas as pd
import numpy as np
import tabulate
# data = {
#     'Patient DataSet': [416, 416, 416, 416, 416, 416, 416, 416, 652, 652, 652, 652],
#     'Hospital': [91, 91, 91, 91, 91, 91, 91, 91, 141, 141, 141, 141],
#     'Method': ['Baseline_ACO', 'Baseline_BCO', 'Baseline_GAO', 'Baseline_ICA', 'ACO', 'BCO', 'GAO', 'ICA', 'Baseline_ACO', 'Baseline_BCO', 'Baseline_GAO', 'Baseline_ICA'],
#     'Final G-score': [34898.5, 34381.5, 34385.0, 34344.0, 34965.5, 34429.0, 34454.0, 34366.0, 54632.5, 53702.5, 53748.0, 53755.5],
#     'Total Delay Time (hours)': [1366.0, 1374.0, 1415.0, 1448.0, 1303.0, 1405.0, 1397.0, 1408.0, 2313.0, 2445.0, 2430.0, 2411.0],
#     'Total Satisfaction (points)': [36001.5, 35994.0, 35967.0, 35932.0, 36065.5, 35972.0, 35988.5, 35961.5, 56320.5, 56191.5, 56208.5, 56232.0],
#     'Total Fatigue (hours)': [1103.0, 1612.5, 1582.0, 1588.0, 1100.0, 1543.0, 1534.5, 1595.5, 1688.0, 2489.0, 2460.5, 2476.5]
# }
data = {
    'Patient DataSet': [416, 416, 416, 416, 416, 416, 416, 416, 652, 652, 652, 652, 652, 652, 652, 652],
    'Hospital': [91, 91, 91, 91, 91, 91, 91, 91, 141, 141, 141, 141, 141, 141, 141, 141],
    'Method': ['Baseline_ACO', 'Baseline_BCO', 'Baseline_GAO', 'Baseline_ICA', 'ACO', 'BCO', 'GAO', 'ICA', 'Baseline_ACO', 'Baseline_BCO', 'Baseline_GAO', 'Baseline_ICA', 'ACO', 'BCO', 'GAO', 'ICA'],
    'Final G-score': [34898.5, 34381.5, 34385.0, 34344.0, 34965.5, 34429.0, 34454.0, 34366.0, 54632.5, 53702.5, 53748.0, 53755.5, 54669.0, 53894.0, 53823.0, 53862.5],
    'Total Delay Time (hours)': [1366.0, 1374.0, 1415.0, 1448.0, 1303.0, 1405.0, 1397.0, 1408.0, 2313.0, 2445.0, 2430.0, 2411.0, 2265.0, 2225.0, 2356.0, 2327.0],
    'Total Satisfaction (points)': [36001.5, 35994.0, 35967.0, 35932.0, 36065.5, 35972.0, 35988.5, 35961.5, 56320.5, 56191.5, 56208.5, 56232.0, 56361.5, 56399.0, 56282.5, 56311.5],
    'Total Fatigue (hours)': [1103.0, 1612.5, 1582.0, 1588.0, 1100.0, 1543.0, 1534.5, 1595.5, 1688.0, 2489.0, 2460.5, 2476.5, 1692.5, 2505.0, 2459.5, 2449.0]
}
df = pd.DataFrame(data)
#
# # Correct Final G-score if necessary
# df['Corrected_Final_G_score'] = df['Total Satisfaction (points)'] - df['Total Fatigue (hours)']
#
# # Calculate new G-scores
# df['Average G-score'] = (df['Total Satisfaction (points)'] / df['Patient DataSet']) - (df['Total Fatigue (hours)'] / df['Hospital'])
# # df['Normalized G-score'] =2500 + (df['Total Satisfaction (points)'] % 90) - df['Total Fatigue (hours)']
# df['G-score 1'] = 0.8 * df['Total Satisfaction (points)'] - 0.2 * df['Total Fatigue (hours)']
# df['G-score 2'] = 0.2 * df['Total Satisfaction (points)'] - 0.8 * df['Total Fatigue (hours)']
# Calculate new G-scores
df['Corrected_FGS'] = df['Total Satisfaction (points)'] - df['Total Fatigue (hours)']
df['AvgG'] = (df['Total Satisfaction (points)'] / df['Patient DataSet']) - (df['Total Fatigue (hours)'] / df['Hospital'])
# df['Normalized_GSc'] = (df['Total Satisfaction (points)'] % 90) - (df['Total Fatigue (hours)'] % 100)
df['GSc1'] = 0.4 * df['Total Satisfaction (points)'] - 0.6 * df['Total Fatigue (hours)']
df['GSc2'] = 0.2 * df['Total Satisfaction (points)'] - 0.8 * df['Total Fatigue (hours)']

df[' Total Fatigue (hours)'] = df['Total Fatigue (hours)']
# Reorder columns
# cols = df.columns.tolist()
# cols = cols[:3] + cols[-5:] + cols[3:6]
# Rename columns
df = df.rename(columns={'Total Delay Time (hours)': 'TDT (hours)',
                       'Total Satisfaction (points)': 'PTS (points)',
                       'Total Fatigue (hours)': 'TFG (hours)',
                       'Final G-score': 'FGS'})


# Reorder columns as requested
cols = ['Patient DataSet', 'Hospital', 'Method', 'TDT (hours)', 'PTS (points)', 'TFG (hours)', 'GSc1', 'GSc2', 'AvgG', 'FGS']
df = df[cols]
# cols = ['Patient DataSet', 'Hospital', 'Method', 'Total Delay Time (hours)', 'Total Satisfaction (points)', 'Total Fatigue (hours)', 'G-score 1', 'G-score 2', 'Average G-score', 'Final G-score']

# df = df[cols]
# Convert to Markdown
markdown_table = df.to_markdown(index=False)
print(markdown_table)
