"""
将fill_blank之后的时间序列片段分割成时间序列片段
注： 需要分析得到切割/插值的时间阈值大小
"""
from TimeSeriesProcess import strip_segment
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

for FileNo in range(1, 4):
    df = pd.read_excel('..\\data\\结果数据文件\\%s_fill.xlsx' % FileNo)
    velocity = df.values[:, 2]
    velocity = velocity.reshape(-1, 1)

    ts_groups = strip_segment(velocity, 180, 30, smooth_flag=False)
    ts_len = np.array([np.log10(len(grp)) for grp in ts_groups])

    plt.figure()
    plt.hist(ts_len, bins=20)
    plt.xlabel('lg(时间序列片段长度)', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
    plt.ylabel('片段数', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
    plt.title('时间序列片段长度分布频率分布直方图', fontdict={'fontsize': 24, 'fontname': 'SimHei'})
    plt.savefig('..\\Figures\\时间序列长度分布图--文件%s' % FileNo)

    # 去除一些时间长度异常的片段
    abnormal_index = np.where((ts_len > ts_len.mean() + ts_len.std() * 3) | (ts_len < ts_len.mean() - ts_len.std() * 3))
    if len(abnormal_index[0]) > 0:
        for ind in reversed(abnormal_index[0]):
            ts_groups.pop(ind)
            ts_len = np.delete(ts_len, ind)

    # 对时间序列的长度进行统计，画分布图
    plt.figure()
    plt.hist(ts_len, bins=20)
    plt.xlabel('lg(时间序列片段长度)', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
    plt.ylabel('片段数', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
    plt.title('时间序列片段长度分布频率分布直方图', fontdict={'fontsize': 24, 'fontname': 'SimHei'})
    plt.savefig('..\\Figures\\时间序列长度分布图(处理后)--文件%s' % FileNo)

    # 保存时间序列
    with open('..\\data\\结果数据文件\\%d_time_series_groups.txt' % FileNo, 'w') as f:
        f.write(str(ts_groups))
    f.close()
