import numpy as np
import pandas as pd
feat_names = ['time', 'v_mean', 'v_max', 'a_max', 'a_min', 'a_mean_a', 'a_mean_d', 'p_i', 'p_c', 'p_a', 'p_d',
              'v_std', 'v_std_no_zero', 'v_mean_no_zero', 'peak_value', 'a_a', 's', 'aver_peak_duration', 'max_peak_duration', 'a_std']

# d_feat_name_en2ch = {'time': '运行时间', 'v_mean': '平均速度', 'v_max': '最大速度', 'a_max': '最大加速度',
#                      'a_min': '最大减速度', 'a_mean_a': '平均加速度', 'a_mean_d': '平均减速度', 'p_i': '怠速比例',
#                      'p_c': '匀速比例', 'p_a': '加速比例', 'p_d': '减速比例', 'v_std': '速度方差',
#                      'v_std_no_zero': '去0速度方差', 'v_mean_no_zero': '去0速度均值', 'peak_value': '峰值个数',
#                       'a_a': '加速度绝对值的平均', 's': '总路程', 'aver_peak_duration': '平均波峰周期',
#                       'max_peak_duration': '最大波峰间隔', 'a_std': '加速度方差'}


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


def feat_ex(ts):
    ts = np.array(ts) / 3.6
    time = len(ts)
    v_mean = np.mean(ts)
    v_max = np.max(ts)
    a_max = np.max([ts[i] - ts[i-1] for i in range(1, time)])
    a_min = np.min([ts[i] - ts[i-1] for i in range(1, time)])
    a_mean_a = np.mean([ts[i] - ts[i-1] for i in range(1, time) if ts[i] - ts[i-1] > 0])
    a_mean_d = np.mean([ts[i] - ts[i - 1] for i in range(1, time) if ts[i] - ts[i - 1] < 0])
    p_i = len(np.where(ts < 0.1)[0]) / time
    t_c = 0
    t_a = 0
    t_d = 0
    for i in range(1, time):
        if ts[i] >= 0.1:
            if abs(ts[i] - ts[i - 1]) < 0.36:
                t_c += 1
            elif ts[i] - ts[i - 1] > 0.36:
                t_a += 1
            else:
                t_d += 1
    p_c = t_c / time
    p_a = t_a / time
    p_d = t_d / time
    v_std = np.std(ts)
    v_std_no_zero = np.std([i for i in ts if i > 0.1])
    v_mean_no_zero = np.mean([i for i in ts if i > 0.1])
    peak_value = cal_peak_value(ts)
    a_a = np.mean([abs(ts[i] - ts[i-1]) for i in range(1, time)])
    s = v_mean * time
    aver_peak_duration, max_peak_duration = cal_peak_duration(ts)
    a_std = np.std(ts[1:] - ts[:-1])
    return [time, v_mean, v_max, a_max, a_min, a_mean_a, a_mean_d, p_i, p_c, p_a, p_d, v_std, v_std_no_zero,
            v_mean_no_zero, peak_value, a_a, s, aver_peak_duration, max_peak_duration, a_std]


if __name__ == '__main__':
    l_all_time = eval(open('..\\..\\data\\结果数据文件\\All_groups_prepared.txt', 'r', encoding='utf-8').read())
    d_feat = {}
    for feat_name in feat_names:
        d_feat[feat_name] = []
    for ts in l_all_time:
        l_feat = feat_ex(ts)
        for i, feat in enumerate(l_feat):
            d_feat[feat_names[i]].append(feat)

    pd.DataFrame(d_feat).to_excel('..\\..\\data\\结果数据文件\\all_feat.xlsx', index=0, encoding='utf-8')
    pd.DataFrame(d_feat).to_excel('..\\..\\data\\最终结果\\all_feat.xlsx', index=0, encoding='utf-8')
