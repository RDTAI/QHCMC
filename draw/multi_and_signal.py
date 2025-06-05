import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Data for different hospitals
data = {
    'method': ['aco', 'bco', 'gao', 'ica', 'QL'],
    '3_hospitals': [
        [4847.0/55- 148.5/44, 13.0, 4847.0/55, 148.5/44],
        [4847.0/55- 175.5/44, 13.0, 4847.0/55, 175.5/44],
        [4849.0/55- 174.0/44, 11.0, 4849.0/55, 174.0/44],
        [4831.0/55- 186.0/44, 29.0, 4831.0/55, 186.0/44],
        [4821.0/55- 194.5/44, 39.0, 4821.0/55, 194.5/44],
    ],
    '2_hospitals': [
        [4799.5/54- 161.5/26, 61.0, 4799.5/54, 161.5/26],
        [4799.0/54- 196.5/26, 61.0, 4799.0/54, 196.5/26],
        [4793.0/54- 202.0/26, 67.0, 4793.0/54, 202.0/26],
        [4754.0/54- 230.0/26, 108.0, 4754.0/54, 230.0/26],
        [4755.0/54- 253.75/26, 106.0, 4755.0/54, 253.75/26],
    ],
    '1_hospital_H1': [
        [4630.0/54- 188.0/11, 236.0, 4630.0/54, 188.0/11],
        [4627.5/54- 224.0/11, 241.0, 4627.5/54, 224.0/11],
        [4625.5/54- 230.0/11, 241.0, 4625.5/54, 230.0/11],
        [4609.0/54- 240.0/11, 263.0, 4609.0/54, 240.0/11],
        [4592.5/54- 284.0/11, 281.0, 4592.5/54, 284.0/11],
    ],
    '1_hospital_H2': [
        [4667.5/54- 186.0/15, 195.0, 4667.5/54, 186.0/15],
        [4656.5/54- 221.0/15, 209.0, 4656.5/54, 221.0/15],
        [4656.5/54- 219.5/15, 210.0, 4656.5/54, 219.5/15],
        [4643.0/54- 230.0/15, 225.0, 4643.0/54, 230.0/15],
        [4618.5/54- 267.0/15, 259.0, 4618.5/54, 267.0/15],
    ]
}

# Create a DataFrame for easier manipulation
df = pd.DataFrame(data)

# Define metrics and their labels
metrics_labels =  ['3 Hospitals', '2 Hospitals', '1 Hospital H1', '1 Hospital H2']
hospital_labels =["Average Final G-score", "Total Delay Time", "Average Patient Satisfaction", "Average Doctor Fatigue"]
bar_width = 0.15  # Width of the bars

# Prepare plotting
fig, axes = plt.subplots(5, 1, figsize=(12, 25))  # Create a figure for 5 methods

# Loop through methods to create bar plots for each
for method_index, method in enumerate(data['method']):
    # Extract the values for each metric across different hospital configurations
    delays = [data['3_hospitals'][method_index][1],
              data['2_hospitals'][method_index][1],
              data['1_hospital_H2'][method_index][1],
              data['1_hospital_H1'][method_index][1]]

    satisfactions = [data['3_hospitals'][method_index][2],
                     data['2_hospitals'][method_index][2],
                     data['1_hospital_H2'][method_index][2],
                     data['1_hospital_H1'][method_index][2]]

    fatigues = [data['3_hospitals'][method_index][3],
                 data['2_hospitals'][method_index][3],
                 data['1_hospital_H2'][method_index][3],
                 data['1_hospital_H1'][method_index][3]]

    scores = [data['3_hospitals'][method_index][0],
              data['2_hospitals'][method_index][0],
              data['1_hospital_H2'][method_index][0],
              data['1_hospital_H1'][method_index][0]]

    # Position of the bars
    x = np.arange(len(hospital_labels))
    colors = ['#A8D8EA',  # Light Blue
              '#EAB8D1',  # Light Pink
              '#D9EBC5',  # Light Green
              '#B2E3E1']  # Light Cyan
    # Create bar plots
    axes[method_index].bar([-0.3,-0.15,0,0.15], scores, width=bar_width, color = colors, label=[' Metrics Comparison Among 3 Hospitals ',' Metrics Comparison Among 2 Hospitals ',' Metrics Comparison Among 1 Hospitals(H2) ',' Metrics Comparison Among 1 Hospitals(H1) '])
    axes[method_index].bar([0.7,0.85,1,1.15], delays, width=bar_width,color = colors)
    axes[method_index].bar([1.7,1.85,2,2.15], satisfactions, width=bar_width,color = colors)
    axes[method_index].bar([2.7,2.85,3,3.15],  fatigues, width=bar_width,color = colors)

    # Customize each subplot
    axes[method_index].set_xticks(x)
    axes[method_index].set_xticklabels(hospital_labels)
    axes[method_index].set_title(f'Metrics for Method: {method}', fontsize=16)
    axes[method_index].set_ylabel('Values', fontsize=12)
    axes[method_index].legend(title='Metrics')



# Adjust layout and display
plt.tight_layout()
plt.show()