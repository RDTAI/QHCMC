import matplotlib.pyplot as plt

# Data for the plot
cycles = [1, 2, 3, 4, 5]
methods = ['aco', 'bco', 'gao', 'ica', 'QL']
delay_times = [
    [4.0, 2.0, 2.0, 3.0, 4.0],  # aco
    [1.0, 8.0, 8.0, 3.0, 3.0],  # bco
    [58.0, 39.0, 46.0, 49.0, 46.0],  # gao
    [16.0, 12.0, 16.0, 8.0, 29.0],  # ica
    [7.0, 9.0, 11.0, 4.0, 5.0]   # QL
]

# Create the plot
plt.figure(figsize=(10, 6))  # Adjust figure size as needed
for i, method in enumerate(methods):
    plt.plot(cycles, delay_times[i], marker='o', label=method)

# Customize the plot
plt.xlabel('Cycle Number')
plt.ylabel('Total Delay Time (hours)')
plt.title('Total Delay Time vs. Cycle Number')
plt.xticks(cycles)  # Ensure all cycle numbers are shown
plt.legend()
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()