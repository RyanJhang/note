import copy
import math
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.fftpack import fft
from scipy.io import wavfile


def get_power_spectrums(samplerate, audio_data):
    n = len(audio_data)
    audio_freq = fft(audio_data)

    freq_range = int(np.ceil((n + 1) / 2.0))
    audio_freq = audio_freq[0:freq_range]  # Half of the spectrum
    mag_freq = np.abs(audio_freq)  # Magnitude
    mag_freq = mag_freq / float(n)

    # power spectrum
    mag_freq = mag_freq ** 2
    if n % 2 > 0:  # ffte odd
        mag_freq[1:len(mag_freq)] = mag_freq[1:len(mag_freq)] * 2
    else:  # fft even
        mag_freq[1:len(mag_freq) - 1] = mag_freq[1:len(mag_freq) - 1] * 2

    # Ts = 1.0/Fs;    # sampling interval 取樣區間
    # freqs = np.arange(0, FreqRange, Ts)  -> 顆粒過細會當機
    freqs = np.arange(0, freq_range, 1.0) * (samplerate / n)
    power_spectrums = 20 * np.log10(mag_freq)

    return freqs, power_spectrums


class CandidateData(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self):
        self.index = []
        self.freqs = []
        self.ps = []


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
    cd = CandidateData()

    curr_f_list = {freq: copy.deepcopy(dict(cd)) for freq in multi_expect_freq if freq <= freqs[-1]}

    for f_index, curr_f in enumerate(freqs):
        target_f = multi_expect_freq[index]

        # 收集區間的freq
        if (target_f - gap) <= curr_f <= (target_f + gap):
            in_range = True
            # curr_f_list.append(power_spectrums[f_index])
            curr_f_list[target_f]["index"].append(f_index)
            curr_f_list[target_f]["freqs"].append(curr_f)
            curr_f_list[target_f]["ps"].append(power_spectrums[f_index])
        else:
            if in_range and curr_f > (target_f + gap):
                index += 1
                if index >= len(multi_expect_freq):
                    break
            in_range = False
    return curr_f_list


def _draw_audio(audio_data, time):
    color = ["b", "g"]
    for ch in range(2):
        plt.subplot(2, 2, ch + 1)
        plt.plot(time, audio_data[:, ch], color[ch], label="{} channel".format(ch))
        plt.legend()
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")


def _draw_power_spectrums(freqs, power_spectrums, ch):
    color = ["b", "g"]
    plt.subplot(2, 2, ch + 3)
    plt.plot(freqs, power_spectrums, color[ch], label="{} channel".format(ch))
    plt.legend()
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power spectrum (dB)")


class PSAndTHD:
    def __init__(self):
        self.freq = []
        self.power_spectrum = []
        self.thd = []


class log:
    def __init__(self):
        self.left = PSAndTHD()
        self.right = PSAndTHD()


def get_square_sum_sqrt(curr_f_list, target_freqs):
    print("target_freqs", target_freqs)

    target_ps = []
    for freq in target_freqs:
        if freq in curr_f_list:
            max_power_spectrums = max(curr_f_list[freq]["ps"]) ** 2
            target_ps.append(max_power_spectrums)
        else:
            target_ps.append(0)

    print("target_ps", target_ps)
    target_sum = sum(target_ps)
    print("target_sum", target_sum)

    target_sqrt = math.sqrt(target_sum)
    print("target_sqrt", target_sqrt)

    return target_sqrt


def calculate_thd(expect_freq, curr_f_list, log: PSAndTHD):
    for freg in expect_freq:

        max_power_spectrums = max(curr_f_list[freg]["ps"])

        log.power_spectrum.append(round(max_power_spectrums, 3))
        index = curr_f_list[freg]["ps"].index(max_power_spectrums)
        log.freq.append(round(curr_f_list[freg]["freqs"][index], 3))

        numerator = freg * np.array([2, 3, 4, 5])
        denominator = freg * np.array([1, 2, 3, 4])
        numerator_sum = get_square_sum_sqrt(curr_f_list, target_freqs=numerator)
        denominator_sum = get_square_sum_sqrt(curr_f_list, target_freqs=denominator)

        # thd = ((p2**2 + p3**2 + pn **2 )) ** 0.5 / ((p1**2 + p2**2 + pn **2)) ** 0.5
        thd = 0 if denominator_sum == 0 else (numerator_sum / denominator_sum)
        thd_persents = "{:.3f}%".format(thd if thd != 0 else 0)
        print(thd_persents)

        log.thd.append(thd_persents)


def save_as_csv(result_log: log, file_path):
    """儲存檔案"""
    # dictionary of lists
    dict = {"freq_left": result_log.left.freq, "power_spectrum_left": result_log.left.power_spectrum, "thd_left": result_log.left.thd,
            "freq_right": result_log.right.freq, "power_spectrum_right": result_log.right.power_spectrum, "thd_right": result_log.right.thd}

    df = pd.DataFrame(dict)
    # saving the dataframe
    df.to_csv(file_path)


def one_channel_flow(samplerate, audio_data_left, expect_freq, gap, ch):
    freqs_left, power_spectrums_left = get_power_spectrums(samplerate, audio_data_left)
    _draw_power_spectrums(freqs_left, power_spectrums_left, ch)

    curr_f_list_left = find_candidate_in_freqs_by_gag(expect_freq, freqs_left, gap, power_spectrums_left)
    result_log_left = PSAndTHD()
    calculate_thd(expect_freq, curr_f_list_left, result_log_left)
    return result_log_left


def main_flow(floder_path: str, file_name: str, gap: int, expect_freq: list):
    # sampling rate 取樣頻率 = 48000
    samplerate, audio_data = wavfile.read(os.path.join(floder_path, file_name))

    audio_data_left, audio_data_right = audio_data[:, 0], audio_data[:, 1]
    # Plot the audio signal in time
    length = audio_data.shape[0] / samplerate
    time = np.linspace(0., length, audio_data.shape[0])
    plt.figure(dpi=100, figsize=(16, 9))
    plt.suptitle(file_name)

    _draw_audio(audio_data, time)

    result_log = log()
    result_log.left = one_channel_flow(samplerate, audio_data_left, expect_freq, gap, 0)
    result_log.right = one_channel_flow(samplerate, audio_data_right, expect_freq, gap, 1)

    save_as_csv(result_log,
                file_path=os.path.join(floder_path, "{}{}".format(file_name.split(".")[0], ".csv")))

    # plt.show()
    plt.savefig(os.path.join(floder_path, "{}{}".format(file_name.split(".")[0], ".png")))
    # Clear the current axes.
    plt.cla()
    # Clear the current figure.
    plt.clf()
    # Closes all the figure windows.
    plt.close('all')


if __name__ == "__main__":

    # file_name = "dut_record_0.wav"
    file_name = "pc_record_0.wav"
    # file_name = "1k_2ch_diff_db.wav"
    # file_name = "mix_tone_16k_8p.wav"
    # file_name = "1K 2CH.wav"

    floder_path = os.path.dirname(os.path.abspath(__file__))
    gap = 1
    expect_freq = [300, 500, 800, 1000, 2000, 3000, 5000, 7500]

    main_flow(floder_path, file_name, gap, expect_freq)
