import numpy as np
import matplotlib.pyplot as plt
# from scipy.signal import find_peaks
from scipy.signal import savgol_filter


# test_dms = np.load('evals/wang/train/dms.npy').squeeze()
# testy = np.load('evals/wang/train/y.npy')
# 0.05641337207263718 0.0473220931384597
# 0.05189274939878535 0.033455590902523306
# qx = test_dms[471]
# test_dms = np.load('evals/wang/test/dms.npy').squeeze()
# testy = np.load('evals/wang/test/y.npy')
# 0.027174723069355148 0.020286203240245854 0.022979016998652076 0.12122908000114739 0.0019511586772812312
# 0.06781540737404013 0.0755508158251359 0.042197863259094484 0.6965990042869878 0.001478511176930775

# qx = test_dms[40]
# test_dms = np.load('evals/blind/dms.npy').squeeze()
# testy = np.load('evals/blind/y.npy')
# qx = test_dms[79]
# q = np.load('npys/q_dm.npy')
# qx = q[1]


def search_dm_peak(dm, fdm, receptive=8, peak_height_ratio=0.1):
    candidate_peaks = []
    len_fdm = len(fdm)
    peak_height_threshold = peak_height_ratio * (np.max(fdm) - np.min(fdm))
    for i in range(receptive): # left and right border
        # left border
        left_local_max = np.max(fdm[:i + receptive + 1])
        if left_local_max == fdm[i]:
            if fdm[i] - np.min(fdm[i + 1 : i + receptive + 1]) > peak_height_threshold:
                if i == 0 or np.max(fdm[:i]) < fdm[i]:
                    candidate_peaks.append(i)
        # right border
        k = len_fdm - i - 1
        right_local_max = np.max(fdm[k - receptive:])
        if right_local_max == fdm[k]:
            if fdm[k] - np.min(fdm[k - receptive : k]) > peak_height_threshold:
                if i == 0 or fdm[k] - np.max(fdm[k + 1:]) > peak_height_threshold:
                    candidate_peaks.append(k)
    for i in range(receptive, len_fdm - receptive):
        left_max = np.max(fdm[i - receptive : i])
        left_min = np.min(fdm[i - receptive : i])
        right_max = np.max(fdm[i + 1 : i + receptive + 1])
        right_min = np.min(fdm[i + 1 : i + receptive + 1])
        if fdm[i] >= left_max and fdm[i] >= right_max:
            # if abs(i - 23) < 5:
            #     print(i, fdm[i], left_max, left_min, right_max, right_min, peak_height_threshold)
            if fdm[i] - left_min > peak_height_threshold and fdm[i] - right_min > peak_height_threshold:
                candidate_peaks.append(i)
            elif fdm[i] - left_min > 0.6 * peak_height_threshold and fdm[i] - right_min > 1.5 * peak_height_threshold:
                candidate_peaks.append(i)
            elif fdm[i] - left_min > 1.5 * peak_height_threshold and fdm[i] - right_min > 0.6 * peak_height_threshold:
                candidate_peaks.append(i)

    # if max peak is at the left border
    if len(candidate_peaks) == 0:
        return [np.argmax(fdm)]
    peak_vals = np.array([-fdm[p] for p in candidate_peaks])
    pv_idxes = np.argsort(peak_vals)
    sorted_peaks = np.array(candidate_peaks)[pv_idxes]
    if sorted_peaks[0] in [0, 1] and len(sorted_peaks) > 1:
        min_dm = np.min(dm)
        if dm[sorted_peaks[1]] > (dm[sorted_peaks[0]] - min_dm) * 0.6 + min_dm:
            return sorted_peaks[1]
    return sorted_peaks[0]

def calc_smoothness(dm, fdm, resolution=20, receptive=50):
    # sampling dm curve
    len_dm = dm.shape[0]
    clear_fdm = []
    for i in range(len_dm - 1):
        clear_fdm.append([i, fdm[i]])
        diffy = fdm[i + 1] - fdm[i]
        for k in range(1, resolution):
            x = k / resolution + i
            y = k * diffy / resolution + fdm[i]
            clear_fdm.append([x, y])
    clear_fdm.append([len_dm - 1, fdm[len_dm - 1]])
    smoothness = 0
    for i, d in enumerate(dm):
        recep_start = max(0, i - receptive)
        recep_end = min(len_dm - 1, i + receptive)
        min_dis = 10^6
        for cfd in clear_fdm:
            if cfd[0] >= recep_start and cfd[0] <= recep_end:
                dis = np.sqrt((cfd[0] - i) ** 2 + (cfd[1] - d) ** 2)
                if dis < min_dis:
                    min_dis = dis
        smoothness += min_dis
    return smoothness / dm.shape[0]

def dm_rules(curve):
    # 入口，输入序列数据，返回DM曲线的峰值x轴位置和平滑度
    # peak == 0 or peak == 1     -->  Negative
    # smoothness > 1.25          -->  Negative
    fdm = savgol_filter(curve, 7, 2)
    # peak = search_dm_peak(curve, fdm, receptive=8, peak_height_ratio=0.1)
    smoothness = calc_smoothness(curve, fdm)
    # positive_miu, positive_sigma = 0.0482, 0.0436
    # negative_miu, negative_sigma = 0.0667, 0.0734
    # positive_guass = np.exp(- (smoothness - positive_miu) ** 2 / 2 / positive_sigma ** 2)
    # negative_guass = np.exp(- (smoothness - negative_miu) ** 2 / 2 / negative_sigma ** 2)
    # smoothness: 宽阈值：2.0-2.8；窄阈值：1.25
    # return peak, smoothness
    return smoothness
def chooseWave(x, min_wave, max_wave):
    index_start = int((min_wave - 900) / (1700 - 900) * 228)
    index_end = int((max_wave - 900) / (1700 - 900) * 228)
    s=[]
    for i in x:
        tmp = i[index_start: index_end]
        s.append(tmp)
    return np.array(s)
def apply_norm(x):
    xi = x
    maxv, minv = max(xi), min(xi)
    list_xi = []
    for xii in xi:
        list_xi.append((xii - minv) / (maxv - minv))
    return np.array(list_xi)
def denoise(x):
    #更新了一个波段选择的函数，因为师兄第二次让做的时候加了这个
    x = chooseWave([x], 1200, 1650)[0]
    x_norm = apply_norm(x)
    dm = dm_rules(x_norm)
    if dm >= 0.01:
        return 0 # 0代表噪声数据
    else:
        return 1 # 1是正常数据

if __name__ == '__main__':
    # 输入x：228
    import numpy as np
    x = np.random.random(228)
    print(denoise(x))