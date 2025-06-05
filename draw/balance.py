# 将 LaTeX 表格转化为 Python 数据
data = {
    '124(26,44)': {'QL Base': [296.75, 288.62], 'QL': [290.75, 292.5]},
    '124(13,26)': {'QL Base': [287.5, 292.0], 'QL': [290.25, 293.5]},
    '144(26,44)': {'QL Base': [350.5, 350.5], 'QL': [354.25, 353.75]},
    '144(13,26)': {'QL Base': [342.62, 343.5], 'QL': [342.25, 348.5]},
    '164(26,44)': {'QL Base': [374.5, 367.87], 'QL': [374.5, 365.0]},
    '164(13,26)': {'QL Base': [363.12, 375.37], 'QL': [365.75, 378.0]},
    '164(44,62)': {'QL Base': [364.5, 375.0], 'QL': [375.75, 364.0]},
    '164(26,44)': {'QL Base': [374.5, 377.25], 'QL': [368.25, 387.25]},
    '184(44,62)': {'QL Base': [400.88, 395.88], 'QL': [393.0, 389.75]},
    '184(26,44)': {'QL Base': [392.38, 401.88], 'QL': [399.5, 395.5]},
    '214(44,62)': {'QL Base': [490.88, 478.13], 'QL': [503.0, 502.75]},
    '214(26,44)': {'QL Base': [477.13, 488.88], 'QL': [492.25, 485.5]}
}

# 计算每一行的医生疲劳度减少百分比并更新原始数据
for case, methods in data.items():
    doctor_counts = tuple(map(int, case.split('(')[1].strip(')').split(',')))
    for method, states in methods.items():
        states[0] = states[0] / doctor_counts[0]
        states[1] = states[1] / doctor_counts[1]
        reduction = (states[0] - states[1]) / states[0] * 100
        states.append(round(reduction, 2))

# 打印结果
print("\\begin{table}[htbp]")
print("\\centering")
print("\\begin{tabular}{lcccccc}")
print("\\toprule")
print("\\multirow{2}{*}{Data} & \multicolumn{3}{c}{QL Base} & \multicolumn{3}{c}{QL} \\\\")
print("\\cmidrule(r){2-4} \\cmidrule(r){5-7}")
print(" & Crowded & Balanced & Reduction & Crowded & Balanced & Reduction \\\\")
print("\\midrule")
for case, methods in data.items():
    print(case, end=" & ")
    print(" & ".join(map(lambda x: "{:.2f}".format(x), methods['QL Base'])), end=" & ")
    print(" & ".join(map(lambda x: "{:.2f}".format(x), methods['QL'])), end=" \\\\\n")
print("\\bottomrule")
print("\\end{tabular}")
print("\\caption{Doctor Fatigue}")
print("\\label{tab:doctor_fatigue}")
print("\\end{table}")
