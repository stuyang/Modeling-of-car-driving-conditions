"""
出一个图，对比滤波前后的结果
"""
from TimeSeriesProcess import smooth_filter, idling_process, acc_abnormal_certify
import matplotlib.pyplot as plt
import numpy as np

# 读取数据
velocity_groups = []
for FileNo in range(3, 4):
    with open('..\\data\\结果数据文件\\%s_time_series_groups.txt' % FileNo, 'r') as f:
        velocity_groups += eval(f.readlines()[0])
    f.close()

# 画图
# fig = plt.figure()
# for i in range(9):
#     ts = velocity_groups[i+13]
#     plt.subplot(3, 3, i + 1)
#     line1 = plt.plot(ts, '--', label='原始速度数据')
#     line2 = plt.plot(smooth_filter(ts, 10), '-.', label='滤波后')
#     plt.legend(loc='best', prop={'size': 10})
#     plt.xlabel('时间', fontdict={'fontsize': 20})
#     plt.ylabel('速度 (km/h)', fontdict={'fontsize': 20})
# plt.suptitle('滤波结果示意图', fontsize=24)
# plt.show()

# 根据时间序列的均速，速度方差和运动时间比例对时间序列进行筛选
aver_v = [sum(grp) / len([item for item in grp if item != 0]) for grp in velocity_groups]
std_v = [np.array(grp).std() for grp in velocity_groups]
run_ratio = [len([item for item in grp if item != 0]) / len(grp) for grp in velocity_groups]

# plt.figure(figsize=(12, 8))
# plt.hist(aver_v, bins=50)
# plt.xlabel('平均速度', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
# plt.ylabel('时间序列片段数', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
# plt.title('时间序列片段的平均速度频率分布直方图', fontdict={'fontsize': 24, 'fontname': 'SimHei'})
# plt.grid(axis='y')
# plt.savefig('..\\Figures\\时间序列平均速度分布图')
# plt.show()
#
# plt.figure(figsize=(12, 8))
# plt.hist(std_v, bins=50)
# plt.xlabel('速度方差', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
# plt.ylabel('时间序列片段数', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
# plt.title('时间序列片段的速度方差频率分布直方图', fontdict={'fontsize': 24, 'fontname': 'SimHei'})
# plt.grid(axis='y')
# plt.savefig('..\\Figures\\时间序列速度方差分布图')
# plt.show()
#
# plt.figure(figsize=(12, 8))
# plt.hist(run_ratio, bins=50)
# plt.xlabel('非零数据比例', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
# plt.ylabel('时间序列片段数', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
# plt.title('时间序列片段的非零数据比例频率分布直方图', fontdict={'fontsize': 24, 'fontname': 'SimHei'})
# plt.grid(axis='y')
# plt.savefig('..\\Figures\\时间序列非零数据比例分布图')
# plt.show()


# 怠速处理+滤波处理+加速度异常处理
fig_id = 0
save_group = []
for ind, grp in enumerate(velocity_groups):
    if (len(grp) > 30) & (aver_v[ind] > 10) & (std_v[ind] > 2) & (run_ratio[ind] > 0.2):
        grp += [0]
        if not acc_abnormal_certify(grp, -28.8, 14.3):
            velocity_no_idle = idling_process(grp, 14.6, 10)
            save_group.append(list(smooth_filter(velocity_no_idle, 3)))
        # else:
        #     plt.figure()
        #     plt.plot(grp, lw=3)
        #     plt.xlabel('时间(s)', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
        #     plt.ylabel('速度(km/h)', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
        #     plt.title('加速度异常片段示意图', fontdict={'fontsize': 24, 'fontname': 'SimHei'})
        #     plt.grid(True)
        #     plt.savefig('..\\Figures\\加速度异常片段示意图_%s' % fig_id)
        #     fig_id += 1
        #     plt.show()
    # if aver_v[ind] < 10:
    #     plt.figure()
    #     plt.plot(grp, lw=3)
    #     plt.xlabel('时间(s)', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
    #     plt.ylabel('速度(km/h)', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
    #     plt.title('平均速度异常示意图', fontdict={'fontsize': 24, 'fontname': 'SimHei'})
    #     plt.grid(True)
    #     plt.savefig('..\\Figures\\平均速度异常示意图_%s' % fig_id)
    #     fig_id += 1
    #     plt.show()
    # if std_v[ind] < 2:
    #     plt.figure()
    #     plt.plot(grp, lw=3)
    #     plt.xlabel('时间(s)', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
    #     plt.ylabel('速度(km/h)', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
    #     plt.title('速度方差异常示意图', fontdict={'fontsize': 24, 'fontname': 'SimHei'})
    #     plt.grid(True)
    #     plt.savefig('..\\Figures\\速度方差异常示意图_%s' % fig_id)
    #     fig_id += 1
    #     plt.show()
    # if run_ratio[ind] < 0.2:
    #     plt.figure()
    #     plt.plot(grp, lw=3)
    #     plt.xlabel('时间(s)', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
    #     plt.ylabel('速度(km/h)', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
    #     plt.title('怠速比例异常示意图', fontdict={'fontsize': 24, 'fontname': 'SimHei'})
    #     plt.grid(True)
    #     plt.savefig('..\\Figures\\怠速比例异常示意图_%s' % fig_id)
    #     fig_id += 1
    #     plt.show()


print("The total number of time series is %d.\n" % len(save_group))

# 保存滤波后的时间序列
with open('..\\data\\结果数据文件\\All_groups_prepared.txt', 'w') as f:
    f.write(str(save_group))
f.close()
