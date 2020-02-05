import numpy as np
from spectral_cluster import spectral_cluster
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.cluster.hierarchy as sch
import seaborn as sns

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


def dis_dtw(x, y):
    """
    find the distance between the time series x and y
    :param x: the first series
    :param y: the second series
    :return: the distance between two series
    """
    m = len(x)
    n = len(y)
    # normalization for x and y
    dmatrix = abs(np.tile(x, [n, 1]).T - np.tile(y, [m, 1]))
    Dmatrix = np.zeros([m, n])
    for i in range(m):
        for j in range(n):
            if (i == 0) & (j == 0):
                Dmatrix[i][j] = dmatrix[i][j]
            elif i == 0:
                Dmatrix[i][j] = Dmatrix[i][j - 1] + dmatrix[i][j]
            elif j == 0:
                Dmatrix[i][j] = Dmatrix[i - 1][j] + dmatrix[i][j]
            else:
                dis1 = Dmatrix[i - 1][j] + dmatrix[i][j]
                dis2 = Dmatrix[i][j - 1] + dmatrix[i][j]
                dis3 = Dmatrix[i - 1][j - 1] + dmatrix[i][j] * 2
                Dmatrix[i][j] = min([dis1, dis2, dis3])
    return Dmatrix[-1][-1] / (m + n - 2)


# 读取数据
distance = np.load('..\\..\\data\\结果数据文件\\dist.npy')
labels = eval(open('..\\..\\data\\最终结果\\时间序列标签结果.txt').read())
ts_groups = eval(open('..\\..\\data\\结果数据文件\\All_groups_prepared.txt', 'r', encoding='utf-8').read())

# 用dtw距离衡量时间序列之间的相似度
# for super_cls in range(3):
#     cls1 = [ind for ind in range(len(labels)) if labels[ind] == super_cls]
#
#     num_cls = 8
#     ts_grp1 = [ts_groups[ind] for ind in cls1]
#     dis_internal = np.array([[distance[i, j] for i in cls1] for j in cls1])
#     fig, ax = plt.subplots(figsize=(12, 8))
#     plt.subplots_adjust(left=0.15, right=0.95, top=0.92, bottom=0.15, wspace=0.3, hspace=0.3)
#     handle = sns.heatmap(dis_internal, ax=ax)
#     ax.set_title('第%d类中的运动学片段之间的dtw距离' % (super_cls + 1), fontdict={'fontsize': 24, 'fontname': 'SimHei'})
#     ax.set_xlabel('运动学片段编号', fontdict={'fontsize': 18, 'fontname': 'SimHei'})
#     ax.set_ylabel('运动学片段编号', fontdict={'fontsize': 18, 'fontname': 'SimHei'})
#     plt.savefig('..\\..\\Figures\\聚类结果图\\第%d类的dtw距离热图' % (super_cls + 1))
#     plt.show()

# 出层次聚类的图
super_cls = 2
cls1 = [ind for ind in range(len(labels)) if labels[ind] == super_cls]
ts_grp1 = [ts_groups[ind] for ind in cls1]
dis_internal = np.array([[distance[i, j] for i in cls1] for j in cls1])
Z = sch.linkage(dis_internal, method='average')
# 将层级聚类结果以树状图表示出来并保存为plot_dendrogram.png
P = sch.dendrogram(Z)
plt.xlabel('时间序列片段号', fontsize=20, fontname='SimHei')
plt.xticks([])
plt.savefig('..\\..\\Figures\\聚类结果图\\类别%s中层次聚类结果图.png' % (super_cls+1))

# 根据linkage matrix Z得到聚类结果:
# cluster = sch.fcluster(Z, t=53, criterion='distance')







