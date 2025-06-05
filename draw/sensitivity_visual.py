import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

experiment_data = [
    # ... (data for a=0.2, b=0.8, a=0.4, b=0.6, a=0.5, b=0.5, a = 0.6, b = 0.4 from previous responses) ...
    #重新跑 指标只需要画 FCFS、 gao Ql MCHC QL的就行了 大概就是同一个数据集，然后变化ab的值变化4-5次，图也不用都花
    #话延迟 疲劳 综合 OTSR 4个 22 排列
    {
        'ab_params': (0.2, 0.8),
        'data': {
            'Method': ['aco', 'bco', 'gao', 'ica', 'QL'],
            'Delay Time': [3.0, 12.0, 4.0, 19.0, 25.0],
            'Satisfaction': [4857.0, 4848.0, 4856.0, 4841.0, 4835.0],
            'Fatigue': [119.0, 144.0, 152.0, 181.0, 155.0],
            'G_score': [76.2, 54.4, 49.6, 23.4, 43.0]
        }
    },
    {
        'ab_params': (0.2, 0.8),
        'data': {
            'Method': ['aco', 'bco', 'gao', 'ica', 'QL'],
            'Delay Time': [2.0, 6.0, 18.0, 13.0, 29.0],
            'Satisfaction': [4858.0, 4854.0, 4842.0, 4847.0, 4831.0],
            'Fatigue': [116.0, 140.5, 148.0, 162.0, 150.0],
            'G_score': [78.8, 58.4, 50.0, 39.8, 46.2]
        }
    },
    {
        'ab_params': (0.2, 0.8),
        'data': {
            'Method': ['aco', 'bco', 'gao', 'ica', 'QL'],
            'Delay Time': [3.0, 2.0, 3.0, 6.0, 18.0],
            'Satisfaction': [4857.0, 4858.0, 4857.0, 4854.0, 4842.0],
            'Fatigue': [116.0, 147.0, 144.0, 157.5, 154.5],
            'G_score': [78.6, 54.0, 56.2, 44.8, 44.8]
        }
    },
        {
        # 'ab_params': (0.4, 0.6),
        'data': {
            'Method': ['aco', 'bco', 'gao', 'ica', 'QL'],
            'Delay Time': [4.0, 5.0, 6.0, 12.0, 31.0],
            'Satisfaction': [4856.0, 4855.0, 4854.0, 4848.0, 4829.0],
            'Fatigue': [118.5, 141.5, 145.0, 160.0, 153.5],
            'G_score': [71.3, 57.1, 54.6, 43.2, 39.5]
        }
    },
    {
        'ab_params': (0.4, 0.6),
        'data': {
            'Method': ['aco', 'bco', 'gao', 'ica', 'QL'],
            'Delay Time': [1.0, 10.0, 3.0, 10.0, 27.0],
            'Satisfaction': [4859.0, 4850.0, 4857.0, 4850.0, 4833.0],
            'Fatigue': [117.0, 145.0, 152.0, 158.5, 158.0],
            'G_score': [73.4, 53.0, 51.6, 44.9, 38.4]
        }
    },
    {
        'ab_params': (0.4, 0.6),
        'data': {
            'Method': ['aco', 'bco', 'gao', 'ica', 'QL'],
            'Delay Time': [2.0, 3.0, 7.0, 10.0, 34.0],
            'Satisfaction': [4858.0, 4857.0, 4853.0, 4850.0, 4826.0],
            'Fatigue': [117.5, 146.0, 145.5, 157.5, 158.75],
            'G_score': [72.7, 55.2, 53.9, 45.5, 35.15]
        }
    },
    {
        'ab_params': (0.5, 0.5),
        'data': {
            'Method': ['aco', 'bco', 'gao', 'ica', 'QL'],
            'Delay Time': [3.0, 5.0, 8.0, 12.0, 30.0],
            'Satisfaction': [4857.0, 4855.0, 4852.0, 4848.0, 4830.0],
            'Fatigue': [118.0, 145.0, 147.0, 159.5, 158.0],
            'G_score': [69.5, 55.0, 52.5, 44.25, 36.0]
        }
    },
    {
        'ab_params':(0.5, 0.5),
        'data': {
            'Method': ['aco', 'bco', 'gao', 'ica', 'QL'],
            'Delay Time': [5.0, 7.0, 6.0, 8.0, 24.0],
            'Satisfaction': [4855.0, 4853.0, 4854.0, 4852.0, 4836.0],
            'Fatigue': [117.0, 149.5, 145.5, 161.5, 154.5],
            'G_score': [69.0, 51.75, 54.25, 45.25, 40.75]
        }
    },
    {
        'ab_params': (0.5, 0.5),
        'data': {
            'Method': ['aco', 'bco', 'gao', 'ica', 'QL'],
            'Delay Time': [3.0, 4.0, 0.0, 19.0, 24.0],
            'Satisfaction': [4857.0, 4856.0, 4860.0, 4841.0, 4836.0],
            'Fatigue': [117.0, 149.5, 151.0, 158.5, 168.75],
            'G_score': [70.0, 53.25, 54.5, 41.25, 33.625]
        }
    },
    {
        'ab_params': (0.6, 0.4),
        'data': {
            'Method': ['aco', 'bco', 'gao', 'ica', 'QL'],
            'Delay Time': [2.0, 3.0, 3.0, 12.0, 15.0],
            'Satisfaction': [4858.0, 4857.0, 4857.0, 4848.0, 4845.0],
            'Fatigue': [117.0, 156.5, 160.5, 163.5, 165.5],
            'G_score': [68.0, 51.6, 50.0, 43.4, 40.8]
        }
    },
    {
        'ab_params': (0.6, 0.4),
        'data': {
            'Method': ['aco', 'bco', 'gao', 'ica', 'QL'],
            'Delay Time': [4.0, 4.0, 5.0, 16.0, 20.0],
            'Satisfaction': [4856.0, 4856.0, 4855.0, 4844.0, 4840.0],
            'Fatigue': [119.0, 153.0, 148.0, 154.5, 161.5],
            'G_score': [66.0, 52.4, 53.8, 44.6, 39.4]
        }
    },
    {
        'ab_params': (0.6, 0.4),
        'data': {
            'Method': ['aco', 'bco', 'gao', 'ica', 'QL'],
            'Delay Time': [3.0, 11.0, 3.0, 13.0, 19.0],
            'Satisfaction': [4857.0, 4849.0, 4857.0, 4847.0, 4841.0],
            'Fatigue': [117.5, 145.0, 145.0, 169.0, 160.5],
            'G_score': [67.2, 51.4, 56.2, 40.6, 40.4]
        }
    },
    {
        'ab_params': (0.8, 0.2),
        'data': {
            'Method': ['aco', 'bco', 'gao', 'ica', 'QL'],
            'Delay Time': [2.0, 3.0, 7.0, 6.0, 23.0],
            'Satisfaction': [4858.0, 4857.0, 4853.0, 4854.0, 4837.0],
            'Fatigue': [117.5, 148.0, 158.0, 162.5, 164.5],
            'G_score': [62.9, 56.0, 50.8, 50.7, 36.7]
        }
    },
    {
        'ab_params': (0.8, 0.2),
        'data': {
            'Method': ['aco', 'bco', 'gao', 'ica', 'QL'],
            'Delay Time': [2.0, 2.0, 10.0, 8.0, 18.0],
            'Satisfaction': [4858.0, 4858.0, 4850.0, 4852.0, 4842.0],
            'Fatigue': [118.0, 148.0, 148.0, 161.0, 165.0],
            'G_score': [62.8, 56.8, 50.4, 49.4, 40.6]
        }
    },
    {
        'ab_params': (0.8, 0.2),
        'data': {
            'Method': ['aco', 'bco', 'gao', 'ica', 'QL'],
            'Delay Time': [3.0, 4.0, 2.0, 11.0, 24.0],
            'Satisfaction': [4857.0, 4856.0, 4858.0, 4849.0, 4836.0],
            'Fatigue': [118.0, 150.0, 155.0, 150.0, 163.5],
            'G_score': [62.0, 54.8, 55.4, 49.2, 36.1]
        }
    }
]

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from scipy.interpolate import make_interp_spline
import matplotlib.cm as cm

# Define a function for a color palette
# Define a function for a color palette from deep to light
def get_color_palette(base_color, num_colors):
    return [cm.get_cmap('Blues')(1 - (i / (num_colors + 1))) for i in range(num_colors)]  # Reverse the color gradient

# Prepare function to convert the nested data structure into a DataFrame
def prepare_data(experiment_data):
    records = []
    for entry in experiment_data:
        ab_params = entry.get('ab_params', None)
        if ab_params:
            for index, method in enumerate(entry['data']['Method']):
                record = {
                    'a_param': ab_params[0],
                    'b_param': ab_params[1],
                    'Method': method,
                    'Delay Time': entry['data']['Delay Time'][index],
                    'Satisfaction': entry['data']['Satisfaction'][index],
                    'Fatigue': entry['data']['Fatigue'][index],
                    'G_score': entry['data']['G_score'][index],
                }
                records.append(record)
    df = pd.DataFrame(records)
    return df


# Function to plot given metric with smooth curves
# def plot_metric(metric, title, ylabel, df, param_sets):
#     # Group by parameter values and method, then calculate metrics
#     df_grouped = df.groupby(['a_param', 'b_param', 'Method']).agg(['mean', 'min', 'max']).reset_index()
#
#     # Create the x-axis labels from provided parameter sets
#     param_labels = [f"({p[0]}, {p[1]})" for p in param_sets]
#
#     # Create plots for each method
#     fig, ax = plt.subplots(figsize=(10, 6))
#
#     for method in df['Method'].unique():
#         method_data = df_grouped[df_grouped['Method'] == method]
#
#         # Ensure we only plot if we have the data for all parameter sets
#         if len(method_data) == len(param_sets):
#             x_values = np.arange(len(param_labels))
#             y_values_mean = method_data[(metric, 'mean')].values
#             y_values_min = method_data[(metric, 'min')].values
#             y_values_max = method_data[(metric, 'max')].values
#
#             # Create a smooth curve using B-spline interpolation
#             x_smooth = np.linspace(min(x_values), max(x_values), 300)
#             spline_mean = make_interp_spline(x_values, y_values_mean, k=3)  # B-spline of order 3
#             y_smooth_mean = spline_mean(x_smooth)
#
#             spline_min = make_interp_spline(x_values, y_values_min, k=3)
#             y_smooth_min = spline_min(x_smooth)
#
#             spline_max = make_interp_spline(x_values, y_values_max, k=3)
#             y_smooth_max = spline_max(x_smooth)
#
#             # Plot the smooth curve
#             ax.plot(x_smooth, y_smooth_mean, label=method, linewidth=2)
#             ax.fill_between(x_smooth, y_smooth_min, y_smooth_max, alpha=0.2)
#
#     ax.set_xticks(x_values)
#     ax.set_xticklabels(param_labels, rotation=45)
#     ax.set_xlabel('Parameter (a, b)')
#     ax.set_ylabel(ylabel)
#     ax.set_title(title)
#     ax.legend()
#     plt.tight_layout()
#     plt.show()


# Define parameter pairs


# Function to plot given metric with smooth curves and cohesive colors
def plot_metric(metric, title, ylabel, df, param_sets):
    # Group by parameter values and method, then calculate metrics
    df_grouped = df.groupby(['a_param', 'b_param', 'Method']).agg(['mean', 'min', 'max']).reset_index()

    # Create the x-axis labels from provided parameter sets
    param_labels = [f"({p[0]}, {p[1]})" for p in param_sets]

    # Create a color palette
    unique_methods = df['Method'].unique()
    colors = get_color_palette('Blues', len(unique_methods))

    # Create plots for each method
    fig, ax = plt.subplots(figsize=(10, 6))

    for color, method in zip(colors, unique_methods):
        method_data = df_grouped[df_grouped['Method'] == method]

        if len(method_data) == len(param_sets):
            x_values = np.arange(len(param_labels))
            y_values_mean = method_data[(metric, 'mean')].values
            y_values_min = method_data[(metric, 'min')].values
            y_values_max = method_data[(metric, 'max')].values

            # Create a smooth curve using B-spline interpolation
            x_smooth = np.linspace(min(x_values), max(x_values), 300)
            spline_mean = make_interp_spline(x_values, y_values_mean, k=3)
            y_smooth_mean = spline_mean(x_smooth)

            # Plot the smooth curve
            ax.plot(x_smooth, y_smooth_mean, label=method, color=color, linewidth=2)

            # Fill between min and max
            spline_min = make_interp_spline(x_values, y_values_min, k=3)
            spline_max = make_interp_spline(x_values, y_values_max, k=3)
            ax.fill_between(x_smooth,
                            spline_min(x_smooth),
                            spline_max(x_smooth),
                            color=color, alpha=0.2)

    ax.set_xticks(x_values)
    ax.set_xticklabels(param_labels, rotation=45)
    ax.set_xlabel('Parameter (a, b)')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    plt.show()


param_sets = [(0.2, 0.8), (0.4, 0.6), (0.5, 0.5), (0.6, 0.4), (0.8, 0.2)]

# Data preparation
df = prepare_data(experiment_data)

# Plot each metric
plot_metric('Delay Time', 'Total Delay Time (hours)', 'Total Delay Time (hours)', df, param_sets)
plot_metric('Satisfaction', 'Total Satisfaction (points)', 'Total Satisfaction (points)', df, param_sets)
plot_metric('Fatigue', 'Total Fatigue (hours)', 'Total Fatigue (hours)', df, param_sets)
plot_metric('G_score', 'Final Comprehensive G-score', 'Final Comprehensive G-score', df, param_sets)

