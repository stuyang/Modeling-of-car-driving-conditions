import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

feat_names = ['v_mean', 'v_drive_mean', 'a_mean_acc', 'a_mean_dec', 'p_idle', 'p_acc', 'p_dec', 'v_std', 'v_drive_std',
              'a_std', 'p_0_25', 'p_25_50', 'p_50_']


def deter_increase(ts):
    for i in range(1, len(ts)):
        if ts[i] < ts[i - 1]:
            return False
    return True


def deter_decrease(ts):
    for i in range(1, len(ts)):
        if ts[i] > ts[i - 1]:
            return False
    return True


def cal_peak_value(ts, gap=5):
    t = 0
    for i in range(gap, len(ts) - gap):
        if deter_increase(ts[i - gap: i + 1]) and deter_decrease(ts[i: i + gap + 1]):
            t += 1
    return t


def cal_peak_duration(ts, gap=5):
    temp_t = 0
    durations = []
    start_flag = False
    for i in range(gap, len(ts) - gap):
        if deter_increase(ts[i - gap: i + 1]) and deter_decrease(ts[i: i + gap + 1]):
            if start_flag:
                durations.append(temp_t)
                temp_t = 0
            else:
                start_flag = True
        else:
            temp_t += 1
    if len(durations) == 0:
        return len(np.where(ts > 0.1)[0]), len(np.where(ts > 0.1)[0])
    else:
        return sum(durations) / len(durations), max(durations)


def feat_extraction2(grps):
    for ind, grp in enumerate(grps):
        grps[ind] = np.array(grp)
    len_ts = sum([len(grp) for grp in grps])
    v_mean = sum([np.sum(grp) for grp in grps]) / len_ts
    p_idle = sum([np.where(grp < 10)[0].shape[0] for grp in grps]) / len_ts
    p_acc = sum([np.where(grp[1:] - grp[:-1] > 1)[0].shape[0] for grp in grps]) / len_ts
    p_dec = sum([np.where(grp[1:] - grp[:-1] < -1)[0].shape[0] for grp in grps]) / len_ts

    v_all = []
    v_drive_all = []
    a_all = []
    for grp in grps:
        v_all += [v for v in grp]
        v_drive_all += [v for v in grp if v > 10]
        a_all += [grp[ind+1] - grp[ind] for ind in range(len(grp)-1)]
    v_std = np.array(v_all).std()
    v_drive_mean = np.array(v_drive_all).mean()
    v_drive_std = np.array(v_drive_all).std()
    a_std = np.array(a_all).std()
    a_mean_acc = np.array([a for a in a_all if a > 0.36]).mean()
    a_mean_dec = np.array([a for a in a_all if a < -0.36]).mean()

    p_0_25 = len([item for item in v_all if item < 25]) / len_ts
    p_25_50 = len([item for item in v_all if 25 <= item < 50]) / len_ts
    p_50_ = len([item for item in v_all if 50 <= item]) / len_ts
    return [v_mean, v_drive_mean, a_mean_acc, a_mean_dec, p_idle, p_acc, p_dec, v_std, v_drive_std, a_std, p_0_25, p_25_50, p_50_]


def feat_extraction(ts):
    len_ts = len(ts)
    ts = np.array(ts)
    v_mean = np.mean(ts)
    v_drive_mean = np.mean([i for i in ts if i > 0.1])
    a_mean_acc = np.mean([ts[i] - ts[i-1] for i in range(1, len_ts) if ts[i] - ts[i-1] > 0.36])
    a_mean_dec = np.mean([ts[i] - ts[i - 1] for i in range(1, len_ts) if ts[i] - ts[i - 1] < -0.36])
    p_idle = np.where(ts < 0.1)[0].shape[0] / len_ts
    p_acc = np.where(ts[1:] - ts[:-1] > 1)[0].shape[0] / len_ts
    p_dec = np.where(ts[1:] - ts[:-1] < -1)[0].shape[0] / len_ts
    v_std = np.std(ts)
    v_drive_std = np.std([i for i in ts if i > 0.1])
    a_std = np.std(ts[1:] - ts[:-1])
    aver_peak_duration = cal_peak_duration(ts)[0]
    p_0_20 = np.where(ts < 20)[0].shape[0] / len_ts
    p_20_40 = len([item for item in ts if (item < 40) & (item >= 20)]) / len_ts
    p_40_60 = len([item for item in ts if (item < 60) & (item >= 40)]) / len_ts
    p_60_ = np.where(ts >= 60)[0].shape[0] / len_ts
    return [v_mean, v_drive_mean, a_mean_acc, a_mean_dec, p_idle, p_acc, p_dec,
            v_std, v_drive_std, a_std, aver_peak_duration, p_0_20, p_20_40, p_40_60, p_60_]


if __name__ == '__main__':
    # 统计每个片段的验证信息
    ts_groups = eval(open('..\\..\\data\\最终结果\\All_groups_prepared.txt', 'r', encoding='utf-8').read())
    d_feat = {item: [] for item in feat_names}
    feat_array = []
    for ts in ts_groups:
        l_feat = feat_extraction2([ts])
        for i, feat in enumerate(l_feat):
            feat_array.append(l_feat)
            d_feat[feat_names[i]].append(feat)
    # 构建的运动学片段的验证信息
    construct_ts = eval(open('..\\..\\data\\最终结果\\构建运动学片段1.txt', 'r').read())
    l_feat = feat_extraction2([construct_ts])
    for i, feat in enumerate(l_feat):
        feat_array.append(l_feat)
        d_feat[feat_names[i]].append(feat)
    pd.DataFrame(d_feat).to_excel('..\\..\\data\\验证结果\\运动学片段验证的验证特征信息.xlsx', index=0, encoding='utf-8')

    actual_feat = feat_extraction2(ts_groups)
    print(actual_feat)
    const_feats = []
    with open('..\\..\\data\\最终结果\\构建运动学片段1.txt', 'r') as f:
        results = f.readlines()
        for result in results:
            ts_constructed = eval(result)
            const_feats.append(feat_extraction2([ts_constructed]))
    const_feats = np.array(const_feats)
    print(const_feats)

    # 计算相对误差
    for file_index, item in enumerate(const_feats):
        relative_error = (item - actual_feat) / actual_feat * 100
        print('\n-------------构建第%d个运动片段的相对误差为: -----------------' % file_index)
        for ind, feat_name in enumerate(feat_names):
            print(feat_name, ': %.1f %%' % relative_error[ind])

    # 最终结果图
    ts_constructed = eval(open('..\\..\\data\\最终结果\\构建运动学片段1.txt', 'r').read())

    plt.figure(figsize=(12, 8))
    plt.plot(ts_constructed, 'b-', lw=3)
    plt.xlabel('时间 (s)', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
    plt.ylabel('速度 (km/h)', fontdict={'fontsize': 20, 'fontname': 'SimHei'})
    plt.title('构建的车辆行驶工况曲线', fontdict={'fontsize': 24, 'fontname': 'SimHei'})
    plt.grid(True)
    plt.savefig('..\\..\\Figures\\构建的车辆行驶工况曲线')
    plt.show()
