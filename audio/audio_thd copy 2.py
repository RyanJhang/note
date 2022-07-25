import copy
import math
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
from scipy.fftpack import fft, fftfreq  # fourier transform
from scipy.io import wavfile  # scipy library to read wav files


def get_thd(abs_data):
    sq_sum = 0.0
    for r in range(len(abs_data)):
       sq_sum = sq_sum + (abs_data[r]) ** 2

    sq_harmonics = sq_sum - (max(abs_data)) ** 2.0
    thd = 100 * sq_harmonics ** 0.5 / max(abs_data)

    return thd


# AudioName = "dut_record_0.wav"  # Audio File
# AudioName = "pc_record_0.wav"  # Audio File
# AudioName = "mix_tone_16k_8p.wav"  # Audio File
AudioName = "1K.wav"  # Audio File
# AudioName = "1K 2CH.wav"  # Audio File

file_path = f'{os.path.dirname(os.path.abspath(__file__))}\\{AudioName}'

# fs = sampling rate 取樣頻率 = 48000
Fs, Audiodata = wavfile.read(file_path)

# Plot the audio signal in time

plt.plot(Audiodata)
plt.title('Audio signal in time', size=16)

# spectrum

n = len(Audiodata)
AudioFreq = fft(Audiodata)

FreqRange = int(np.ceil((n + 1) / 2.0))
AudioFreq = AudioFreq[0:FreqRange]  # Half of the spectrum
MagFreq = np.abs(AudioFreq)  # Magnitude
MagFreq = MagFreq / float(n)
# power spectrum
MagFreq = MagFreq ** 2
if n % 2 > 0:  # ffte odd
    MagFreq[1:len(MagFreq)] = MagFreq[1:len(MagFreq)] * 2
else:  # fft even
    MagFreq[1:len(MagFreq) - 1] = MagFreq[1:len(MagFreq) - 1] * 2

# Ts = 1.0/Fs;    # sampling interval 取樣區間
# freqs = np.arange(0, FreqRange, Ts)  -> 顆粒過細會當機
freqs = np.arange(0, FreqRange, 1.0) * (Fs / n)
# freqs = np.arange(0, int(np.ceil((n + 1) / 2.0)), 1.0) * 1
power_spectrums = 20 * np.log10(MagFreq)


plt.figure()
plt.plot(freqs, power_spectrums)  # Power spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power spectrum (dB)')
plt.title(f"{AudioName}")
plt.show()


expect_freq = [300, 500, 800, 1000, 2000, 3000, 5000, 7500]


def find_candidate_in_freqs_by_gag(expect_freq, freqs, gap, power_spectrums):
    # expect_freq 需要擴展，因為THD計算需要 往後5個倍數頻率
    def extend_freqs_for_thd(expect_freq):
        multi_expect_freq = []
        for freq in expect_freq:
            multi_expect_freq.extend(freq * np.array([1, 2, 3, 4, 5]))
        return sorted(set(multi_expect_freq))

    multi_expect_freq = extend_freqs_for_thd(expect_freq)

    index = 0
    in_range = False
    a = {"index": [],
         "ps_left": [],
         "ps_right": [],
         "freqs": []}

    curr_f_list = {freq: copy.deepcopy(a) for freq in multi_expect_freq if freq <= freqs[-1]}

    for f_index, curr_f in enumerate(freqs):
        target_f = multi_expect_freq[index]

        # 收集區間的freq
        if (target_f - gap) <= curr_f <= (target_f + gap):
            in_range = True
            # curr_f_list.append(power_spectrums[f_index])
            curr_f_list[target_f]["index"].append(f_index)
            curr_f_list[target_f]["freqs"].append(curr_f)
            curr_f_list[target_f]["ps_left"].append(power_spectrums[f_index][0])
            curr_f_list[target_f]["ps_right"].append(power_spectrums[f_index][1])
        else:
            if in_range and curr_f > (target_f + gap):
                index += 1
                if index >= len(multi_expect_freq):
                    break
            in_range = False
    return curr_f_list


def get_square_sum_sqrt1(freqs, power_spectrums, target_freqs):
    print("target_freqs", target_freqs)
    target_ps = []
    for freq in target_freqs:
        # step 1 if target_freq in freqs
        if freq in freqs:
            index = list(freqs).index(freq)
            if power_spectrums[index] in [float("inf"), float("-inf")]:
                count = 0
                sums = 0
                for shift in [-1, 0, 1]:
                    if index + shift > len(power_spectrums) - 1:
                        continue
                    shift_ps = power_spectrums[index + shift]
                    if shift_ps not in [float("inf"), float("-inf")]:
                        sums += shift_ps
                        count += 1

                target_ps.append((sums / count) ** 2)
            else:
                target_ps.append(power_spectrums[index] ** 2)

        else:
            target_ps.append(0)

    print("target_ps", target_ps)
    target_sum = sum(target_ps)
    print("target_sum", target_sum)

    target_sqrt = math.sqrt(target_sum)
    print("target_sqrt", target_sqrt)

    return target_sqrt


def get_square_sum_sqrt(side, curr_f_list, target_freqs):
    print("target_freqs", target_freqs)

    target_ps = []
    for freq in target_freqs:
        if freq in curr_f_list:
            max_power_spectrums = max(curr_f_list[freq][side]) ** 2
            target_ps.append(max_power_spectrums)
        else:
            target_ps.append(0)

    print("target_ps", target_ps)
    target_sum = sum(target_ps)
    print("target_sum", target_sum)

    target_sqrt = math.sqrt(target_sum)
    print("target_sqrt", target_sqrt)

    return target_sqrt


gap = 1
curr_f_list = find_candidate_in_freqs_by_gag(expect_freq, freqs, gap, power_spectrums)


class PSAndTHD:
    def __init__(self):
        self.freq = []
        self.power_spectrum = []
        self.thd = []


class log:
    def __init__(self):
        self.left = PSAndTHD()
        self.right = PSAndTHD()


result_log = log()


def calculate_thd(expect_freq, side, curr_f_list, log: PSAndTHD):
    for freg in expect_freq:

        max_power_spectrums = max(curr_f_list[freg][side])

        log.power_spectrum.append(round(max_power_spectrums, 3))
        index = curr_f_list[freg][side].index(max_power_spectrums)
        log.freq.append(round(curr_f_list[freg]["freqs"][index], 3))

        numerator = freg * np.array([2, 3, 4, 5])
        denominator = freg * np.array([1, 2, 3, 4])
        numerator_sum = get_square_sum_sqrt(side, curr_f_list, target_freqs=numerator)
        denominator_sum = get_square_sum_sqrt(side, curr_f_list, target_freqs=denominator)

        # thd = ((p2**2 + p3**2 + pn **2 )) ** 0.5 / ((p1**2 + p2**2 + pn **2)) ** 0.5
        thd = 0 if denominator_sum == 0 else (numerator_sum / denominator_sum)
        thd_persents = "{:.3f}%".format(thd if thd != 0 else 0)
        print(thd_persents)

        log.thd.append(thd_persents)


def save_as_csv(result_log: log, file_path):
    """儲存檔案"""
    # dictionary of lists
    dict = {'freq_left': result_log.left.freq, 'power_spectrum_left': result_log.left.power_spectrum, 'thd_left': result_log.left.thd,
            'freq_right': result_log.right.freq, 'power_spectrum_right': result_log.right.power_spectrum, 'thd_right': result_log.right.thd}

    df = pd.DataFrame(dict)
    # saving the dataframe
    df.to_csv(file_path)


calculate_thd(expect_freq, "ps_left", curr_f_list, result_log.left)
calculate_thd(expect_freq, "ps_right", curr_f_list, result_log.right)

save_as_csv(result_log,
            file_path=f'{os.path.dirname(os.path.abspath(__file__))}\\{AudioName}.csv')


#Spectrogram

# N = 512  # Number of point in the fft
# f, t, Sxx = signal.spectrogram(Audiodata, fs, window=signal.blackman(N), nfft=N)
# plt.figure()
# plt.pcolormesh(t, f, 20*np.log10(Sxx))  # dB spectrogram
# #plt.pcolormesh(t, f,Sxx) # Lineal spectrogram
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [seg]')
# plt.title('Spectrogram with scipy.signal', size=16)
