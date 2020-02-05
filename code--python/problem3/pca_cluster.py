import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


df = pd.read_excel('..\\..\\data\\最终结果\\all_feat.xlsx', encoding='utf-8')
x = df.values

scaler = MinMaxScaler()
x = scaler.fit_transform(x)
pca = PCA(n_components=x.shape[1])
x_pca = pca.fit_transform(x)

# 画主成分的累积方差解释比例
# num_feat = x.shape[1]
# plt.figure(figsize=(12, 8))
# plt.plot(np.cumsum(np.hstack(([0], pca.explained_variance_ratio_))), 'bs-', markersize=10, lw=3)
# plt.plot(np.linspace(0, num_feat, num_feat), np.ones(num_feat) * 0.9, 'r--', lw=2)
# plt.xlabel('主成分个数', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
# plt.ylabel('累计方差比例', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
# plt.xlim((0, num_feat))
# plt.ylim((0, 1.1))
# plt.title('PCA累计方差贡献率比例图', fontdict={'fontsize': 24, 'fontname': 'SimHei'})
# plt.grid(True)
# plt.savefig('..\\..\\Figures\\PCA累计方差贡献率图')
# plt.show()


l_k = range(1, 10)
l_sse = []
for k in l_k:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(x_pca)
    l_sse.append(kmeans.inertia_)

# plt.figure(figsize=(12, 8))
# plt.plot(l_k, l_sse, 'bo-', markersize=10, lw=3)
# plt.xlabel('聚类数 k', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
# plt.ylabel('SSE指标', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
# plt.xlim((0, max(l_k)))
# plt.ylim((min(l_sse) * 0.9, max(l_sse) * 1.1))
# plt.title('Kmeans方法中SSE指标随聚类数变化的变化趋势图', fontdict={'fontsize': 24, 'fontname': 'SimHei'})
# plt.grid(True)
# plt.savefig('..\\..\\Figures\\Kmeans方法中SSE指标随聚类数变化的变化趋势图')
# plt.show()


all_ts = eval(open('..\\..\\data\\结果数据文件\\All_groups_prepared.txt', 'r', encoding='utf-8').read())
num_k = 3
kmeans = KMeans(n_clusters=num_k)
kmeans.fit(x_pca)
pred_labels = list(kmeans.labels_)


# N = 4
# for class_label in range(num_k):
#     plt.figure(figsize=(12, 8))
#     plt.subplots_adjust(left=0.1, right=0.95, top=0.92, bottom=0.1, wspace=0.3, hspace=0.3)
#     fig_index = 0
#     for j, label in enumerate(kmeans.labels_):
#         if fig_index > N ** 2 - 1:
#             break
#         if label == class_label:
#             fig_index += 1
#             plt.subplot(N, N, fig_index)
#             plt.plot(all_ts[j], lw=2)
#             if fig_index > (N-1) * N:
#                 plt.xlabel('时间', fontdict={'fontsize': 16, 'fontname': 'SimHei'})
#             if np.mod(fig_index, N) == 1:
#                 plt.ylabel('速度 (km/h)', fontdict={'fontsize': 16, 'fontname': 'SimHei'})
#             plt.ylim((0, 70))
#             plt.grid(True)
#     plt.suptitle('类别%s中的部分运动学片段' % (class_label+1), fontsize=24)
#     plt.savefig('..\\..\\Figures\\聚类结果图\\类别%s中的部分运动学片段' % class_label)
#     plt.show()


# 标签写入txt
with open('..\\..\\data\\最终结果\\时间序列标签结果.txt', 'w') as f:
    f.write(str(pred_labels))
f.close()
print({cls: pred_labels.count(cls) for cls in range(num_k)})
print(list(kmeans.labels_))

# 计算样本到聚类中心距离
dis_result = [[] for i in range(num_k)]
centers = kmeans.cluster_centers_
for n_samp in range(x.shape[0]):
    for cls in range(num_k):
        if pred_labels[n_samp] == cls:
            temp_dis = sum((x[n_samp] - centers[cls]) ** 2)
            dis_result[cls].append({n_samp: temp_dis})

with open('..\\..\\data\\最终结果\\样本距离聚类中心距离.txt', 'w') as f:
    f.write(str(dis_result))
f.close()

