import matplotlib.pyplot as plt

# Data for the plot.  Each inner list represents a method's delays across different surgical_time_delay_factors.
delay_times = [
    [2.0, 2.0, 1.0, 2.0, 2.0],  # aco
    [9.0, 6.0, 0.0, 8.0, 4.0],  # bco
    [50.0, 36.0, 50.0, 63.0, 50.0],  # gao
    [17.0, 4.0, 32.0, 16.0, 16.0],  # ica
    [14.0, 11.0, 4.0, 11.0, 14.0]   # QL
]

methods = ['aco', 'bco', 'gao', 'ica', 'QL']

#Representing surgical_time_delay_factors.  You'll need to replace this with more meaningful representations.  This example simply uses sequential numbers.
x_values = range(1, len(delay_times[0]) + 1)

# Create the plot
plt.figure(figsize=(10, 6))
for i, method in enumerate(methods):
    plt.plot(x_values, delay_times[i], marker='o', label=method)

# Customize the plot
plt.xlabel('Surgical Time Delay Factor Configuration') # You should replace this with more descriptive labels based on your actual configurations
plt.ylabel('Total Delay Time (hours)')
plt.title('Total Delay Time vs. Surgical Time Delay Factors')
plt.xticks(x_values)
plt.legend()
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()