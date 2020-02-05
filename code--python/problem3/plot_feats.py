import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

df = pd.read_excel('..\\..\\data\\结果数据文件\\all_feat.xlsx')
feat_name_dict = {'time': '运动学片段长度', 'v_mean': '平均速度', 'v_max': '最大速度', 'a_max': '最大加速度',
                  'a_min': '最大减速度', 'a_mean_a': '平均加速度', 'a_mean_d': '平均减速度', 'p_i': '怠速时间比例',
                  'p_c': '匀速时间比例', 'p_a': '加速时间比例', 'p_d': '减速时间比例', 'v_std': '速度标准差',
                  'v_std_no_zero': '行驶速度标准差', 'v_mean_no_zero': '平均行驶速度', 'peak_value': '峰值个数',
                  'a_a': '平均绝对加速度', 's': '总行驶路程', 'aver_peak_duration': '平均波峰间隔',
                  'max_peak_duration': '最大波峰间隔', 'a_std': '加速度标准差'}


xlabel_dict = {'time': '运动学片段长度', 'v_mean': '平均速度 (m/s)', 'v_max': '最大速度 (m/s)', 'a_max': '最大加速度 (m/s^2)',
                  'a_min': '最大减速度 (m/s^2)', 'a_mean_a': '平均加速度 (m/s^2)', 'a_mean_d': '平均减速度 (m/s^2)', 'p_i': '怠速时间比例',
                  'p_c': '匀速时间比例', 'p_a': '加速时间比例', 'p_d': '减速时间比例', 'v_std': '速度标准差',
                  'v_std_no_zero': '行驶速度标准差', 'v_mean_no_zero': '平均行驶速度 (m/s)', 'peak_value': '峰值个数',
                  'a_a': '平均绝对加速度 (m/s^2)', 's': '总行驶路程 (m)', 'aver_peak_duration': '平均波峰间隔 (s)',
                  'max_peak_duration': '最大波峰间隔 (s)', 'a_std': '加速度标准差'}

for feat_name in df.columns:
    plt.figure()
    data = df[feat_name]
    plt.hist(data, bins=50)
    plt.xlabel(xlabel_dict[feat_name], fontdict={'fontsize': 16, 'fontname': 'SimHei'})
    plt.ylabel('运动学片段数', fontdict={'fontsize': 18, 'fontname': 'SimHei'})
    plt.title('运动学片段的%s分布图' % feat_name_dict[feat_name], fontdict={'fontsize': 24, 'fontname': 'SimHei'})
    plt.grid(axis='y')
    plt.savefig('..\\..\\Figures\\Problem3时间序列基本信息统计\\时间序列%s分布图' % feat_name_dict[feat_name])
plt.show()

