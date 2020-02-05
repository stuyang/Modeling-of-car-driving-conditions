"""
绘制时间序列片段的统计结果信息
"""
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

# 读取数据
with open('..\\..\\data\\结果数据文件\\All_groups_prepared.txt', 'r') as f:
    velocity_groups = eval(f.readlines()[0])
f.close()

temp = [item if item > 0 else 0 for item in velocity_groups[1]]
plt.figure()
plt.plot(temp, lw=3)
plt.xlabel('速度 (km/h)', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
plt.ylabel('时间 (s)', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
plt.grid(True)
plt.show()

# 时间序列长度分布图
len_ts = [len(grp) for grp in velocity_groups]
plt.figure(figsize=(12, 8))
plt.hist(len_ts, bins=50)
plt.xlabel('时间序列长度', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
plt.ylabel('时间序列片段数', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
plt.title('时间序列片段的长度分布直方图', fontdict={'fontsize': 24, 'fontname': 'SimHei'})
plt.grid(axis='y')
plt.savefig('..\\..\\Figures\\时间序列长度分布图')
plt.show()


# 时间序列的个数
print('总的时间序列片段数为 %d 个!' % len(velocity_groups))


# 画其中九个时间序列片段
plt.figure(figsize=(16, 9))
plt.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.1, wspace=0.3, hspace=0.3)
for ind in range(9):
    plt.subplot(3, 3, ind+1)
    plt.plot(velocity_groups[ind], lw=3)
    plt.xlabel('速度 (km/h)', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
    plt.ylabel('时间 (s)', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
    plt.grid(True)
plt.suptitle('部分速度时间序列片段', fontsize=24)
plt.savefig('..\\..\\Figures\\部分时间序列片段图')
plt.show()
