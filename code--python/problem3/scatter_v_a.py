"""
绘制v-a分布散点图
"""
import matplotlib.pyplot as plt
import seaborn as sns


# 读取数据
with open('..\\..\\data\\结果数据文件\\All_groups_prepared.txt', 'r') as f:
    velocity_groups = eval(f.readlines()[0])
f.close()

# print(len(velocity_groups))
# 1676组

# for grp in velocity_groups:
#     if len(grp) > 300:
#         plt.plot(grp)
#         plt.show()

a_rec = []
v_rec = []
for grp in velocity_groups:
    for ind in range(len(grp)-1):
        if grp[ind] > 3:
            a_rec.append(grp[ind+1] - grp[ind])
            v_rec.append(grp[ind])


# plt.figure()
# plt.plot(a_rec)
# plt.plot(v_rec)
# plt.show()


plt.figure()
plt.scatter(v_rec, a_rec, linewidths=0.1, marker='.')
plt.xlabel('速度', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
plt.ylabel('加速度', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
plt.title('车辆行驶过程中速度-加速度特征分布散点图', fontdict={'fontsize': 24, 'fontname': 'SimHei'})
plt.grid(True)
plt.savefig('..\\..\\Figures\\速度-加速度分布散点图')
plt.show()


v_rec = v_rec[: 1000]
a_rec = a_rec[: 1000]

plt.figure()
h = sns.jointplot(v_rec, a_rec, kind='kde')
h.set_axis_labels('速度', '加速度', fontsize=20, fontname='SimHei')
plt.savefig('..\\..\\Figures\\速度-加速度特征分布核密度估计图')
plt.show()
