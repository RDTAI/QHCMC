import matplotlib.pyplot as plt

# Data for the plot
alpha_beta_values = [(0.2, 0.8), (0.4, 0.6), (0.5, 0.5), (0.6, 0.4), (0.8, 0.2)]
methods = ['aco', 'bco', 'gao', 'ica', 'QL']
delay_times = [
    [4.0, 2.0, 6.0, 6.0, 0.0],  # aco
    [17.0, 1.0, 5.0, 5.0, 3.0],  # bco
    [58.0, 58.0, 51.0, 54.0, 43.0],  # gao
    [13.0, 22.0, 20.0, 21.0, 11.0],  # ica
    [12.0, 11.0, 16.0, 18.0, 9.0]   # QL
]

# Create x-axis ticks as a sequence
x_ticks = range(len(alpha_beta_values))

# Create the plot
plt.figure(figsize=(10, 6))
for i, method in enumerate(methods):
    plt.plot(x_ticks, delay_times[i], marker='o', label=method)

# Customize the plot
plt.xlabel(r'$(\alpha, \beta)$ Values')
plt.ylabel('Total Delay Time (hours)')
plt.title('Total Delay Time vs. Hyperparameters -- $alpha, beta$')
plt.xticks(x_ticks, [str(ab) for ab in alpha_beta_values])  # Set x-axis ticks and labels
plt.legend()
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()