import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


data = pd.read_excel('..\\..\\data\\验证结果\\运动学片段验证的验证特征信息.xlsx').values
n_feat = data.shape[1]

actual_data = data[:-1, :]
construct_data = data[-1, :]

mean_actual = np.mean(actual_data, axis=0)
std_actual = np.std(actual_data, axis=0)

xf = np.linspace(0, n_feat-1, n_feat)
lb = mean_actual - 1.95 * std_actual
ub = mean_actual + 1.95 * std_actual


plt.figure()
plt.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.2, wspace=0.3, hspace=0.3)
plt.fill_between(xf, lb, ub, color='blue', alpha=0.2, lw=0)
plt.plot(xf, construct_data, 'b', lw=2)
plt.xticks(np.linspace(0, n_feat-1, n_feat), ['平均速度', '平均行驶速度', '平均加速度', '平均减速度', '怠速时间比例', '加速时间比例',
                                              '减速时间比例', '速度标准差',	'行驶速度标准差', '加速度标准差', '0-25km/h速度比例',
                                              '25-50km/h速度比例', '50km/h以上速度比例'], rotation=45, fontsize=12)

plt.grid(axis='x')
plt.show()
