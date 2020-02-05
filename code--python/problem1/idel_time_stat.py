"""
对idle时间宽度进行统计，查找最合理的idle时间长度阈值
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False


def idling_stat(ts_velocity, threshold):
    """
    怠速状态检测，并将其置零
    :param ts_velocity: 速度时间序列
    :param threshold: 低于该速度认为进入怠速状态
    :return:  处理后的时间序列
    """
    len_ts = len(ts_velocity)
    delta_t = 0
    record_idle = []
    for tk in range(len_ts):
        if (ts_velocity[tk] < threshold) & (ts_velocity[tk] > 0):
            delta_t += 1
        else:
            if delta_t > 0:
                record_idle.append(delta_t)
                delta_t = 0
    return record_idle


all_record = []

# 读取数据
for FileNo in range(1, 4):
    with open('..\\data\\结果数据文件\\%s_time_series_groups.txt' % FileNo, 'r') as f:
        velocity_groups = eval(f.readlines()[0])
    f.close()
    for grp in velocity_groups:
        all_record += idling_stat(grp, 10)

plt.figure(figsize=(12, 8))
plt.hist(all_record, bins=30)
# x = np.linspace(2, 80, 100)
# lamd = 1/0.5
# plt.plot(x, lamd * np.exp(-lamd * x) * (x[1]-x[0]) * len(all_record))
# sns.distplot(all_record, bins=30, kde_kws={"color": "r", "lw": 2}, hist_kws={"color": '#0000FF'})
plt.xlabel('怠速时间', fontdict={'fontsize': 20})
plt.ylabel('出现频次', fontdict={'fontsize': 20})
plt.title('怠速时间长度分布图', fontsize=24)
plt.grid(axis='y')
plt.savefig('..\\Figures\\怠速时间长度分布图.png')
plt.show()

print('The expectation is %.2f.' % (sum(all_record)/len(all_record)))
# 结论： 怠速状态的时间阈值为3*4.87 = 14.6 (95%置信区间)
