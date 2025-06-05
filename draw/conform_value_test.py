import pandas as pd

data = {
    'Method': ['QL'],
    'Total Delay Time (hours)': [24.0],
    'Total Satisfaction (points)': [4836.0],
    'Total Fatigue (hours)': [163.5],
    'Final Comprehensive G-score': [3836.8]
}

df = pd.DataFrame(data)

# Calculate G-score using the proposed formula
df['Calculated G-score'] = 0.8 * df['Total Satisfaction (points)'] - 0.2 * df['Total Fatigue (hours)']

# Compare calculated and reported G-scores
df['Difference'] = df['Final Comprehensive G-score'] - df['Calculated G-score']

print(df)