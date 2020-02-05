import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import copy

mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False


def strip_segment(ts_velocity, max_idel_period, min_len, smooth_flag):
    """
    对速度时间序列进行分割，怠速时间超过最大怠速时间的按最大怠速时间处理
    :param ts_velocity: 速度时间序列
    :param max_idel_period: 最大怠速时间
    :param min_len: 最小时间序列长度，短于此长度的时间序列不做记录
    :param smooth_flag: 滤波处理标志位
    :return:
    """
    strips = []
    len_ts = ts_velocity.shape[0]
    ts_velocity = copy.copy(ts_velocity)
    start_ind = 0
    for ind in range(1, len_ts-1):
        if (ts_velocity[ind, 0] == 0) & (ts_velocity[ind-1, 0] > 0):
            temp_ts = ts_velocity[start_ind:ind+1, 0]
            del_ind = max(np.where(temp_ts > 0)[0][0] - max_idel_period, 0)
            if smooth_flag:
                strips.append(list(smooth_filter(temp_ts[del_ind:].reshape(-1, 1), 10)))
            else:
                strips.append(list(temp_ts[del_ind:].reshape(-1)))
            start_ind = ind
    return strips


def idling_process(ts_velocity, idle_period, threshold):
    """
    怠速状态检测，并将其置零
    :param ts_velocity: 速度时间序列
    :param idle_period: 低速时间超过该时间，认为进入idle状态
    :param threshold: 低于该速度认为进入怠速状态
    :return:  处理后的时间序列
    """
    ts_velocity = np.array(ts_velocity).reshape(-1, 1)
    len_ts = len(ts_velocity)
    idle_flag = False
    start_ind = 0
    record_idle = []
    for tk in range(len_ts):
        if (not idle_flag) & (ts_velocity[tk] < threshold) & (ts_velocity[tk] > 0):
            idle_flag = True
            start_ind = tk
        elif idle_flag & (ts_velocity[tk] > threshold):
            idle_flag = False
            if (tk - start_ind) >= idle_period:
                record_idle += range(start_ind, tk)
    ts_velocity[record_idle] = 0
    return ts_velocity


def smooth_filter(ts_velocity, C):
    """
    对数据进行滤波
    :param ts_velocity: 速度时间序列
    :param C: 滤波因子C
    :return: 滤波完的数据
    """
    n_sample = len(ts_velocity)
    M = np.zeros((n_sample, n_sample))
    for i in range(n_sample):
        if i == 0:
            M[i, :3] = [1, -2, 1]
        elif i == 1:
            M[i, :4] = [-2, 5, -4, 1]
        elif i == n_sample-2:
            M[i, n_sample-4:] = [1, -4, 5, -2]
        elif i == n_sample-1:
            M[i, n_sample-3:] = [1, -2, 1]
        else:
           M[i, i-2:i+3] = [1, -4, 6, -4, 1]
    return np.linalg.inv(np.eye(n_sample) + C*M).dot(ts_velocity).reshape(-1)


def fill_data(df, threshold):
    df['时间'] = df['时间'].apply(lambda x: x.split('.')[0])
    df['time'] = pd.to_datetime(df['时间'], format='%Y/%m/%d %H:%M:%S')
    helper = pd.DataFrame({'time': pd.date_range(df['time'].min(), df['time'].max(), freq='S')})
    df = pd.merge(df, helper, on='time', how='outer').sort_values('time')[['time', 'GPS车速']]
    t = 0
    for i, v in enumerate(df['GPS车速'].isnull()):
        if v:
            t += 1
        else:
            if t > threshold:
                df['GPS车速'].iloc[i - t: i] = 0
            t = 0
    df['GPS车速'] = df['GPS车速'].interpolate(method='linear')
    return df


# acc_abnormal_certify(ts, -28.8, 14.3)
def acc_abnormal_certify(ts, lb, ub):
    for i in range(1, len(ts)):
        if ts[i] - ts[i - 1] >= ub or ts[i] - ts[i - 1] <= lb:
            return True
    return False


# df1 = pd.read_excel('..\\data\\原始数据\\test.xlsx', encoding='utf8')
# df1_fill = fill_data(df1, 10)
# df1_fill.to_excel('..\\data\\结果数据文件\\1_fill.xlsx', encoding='utf-8')



