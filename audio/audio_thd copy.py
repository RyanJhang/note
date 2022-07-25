from scipy import signal
from scipy.fftpack import fft, fftfreq  # fourier transform
import matplotlib.pyplot as plt
import os
import math

import numpy as np
from scipy.io import wavfile  # scipy library to read wav files

import pandas as pd


def save_as_csv(freq, power_spectrum, thd, file_path):
    """儲存檔案"""

    # list of name, degree, score

    # dictionary of lists
    dict = {'freq': freq, 'power_spectrum': power_spectrum, 'thd': thd}

    df = pd.DataFrame(dict)
    # saving the dataframe
    df.to_csv(file_path)


def get_thd(abs_data):
    sq_sum = 0.0
    for r in range(len(abs_data)):
       sq_sum = sq_sum + (abs_data[r])**2

    sq_harmonics = sq_sum - (max(abs_data))**2.0
    thd = 100*sq_harmonics**0.5 / max(abs_data)

    return thd


AudioName = "dut_record_0.wav"  # Audio File

file_path = f'{os.path.dirname(os.path.abspath(__file__))}\\{AudioName}'
fs, Audiodata = wavfile.read(file_path)

# Plot the audio signal in time

plt.plot(Audiodata)
plt.title('Audio signal in time', size=16)

# spectrum

n = len(Audiodata)
AudioFreq = fft(Audiodata)
AudioFreq = AudioFreq[0:int(np.ceil((n + 1) / 2.0))]  # Half of the spectrum
MagFreq = np.abs(AudioFreq)  # Magnitude
MagFreq = MagFreq / float(n)
# power spectrum
MagFreq = MagFreq**2
if n % 2 > 0:  # ffte odd
    MagFreq[1:len(MagFreq)] = MagFreq[1:len(MagFreq)] * 2
else:  # fft even
    MagFreq[1:len(MagFreq) - 1] = MagFreq[1:len(MagFreq) - 1] * 2

plt.figure()
freqs = np.arange(0, int(np.ceil((n + 1) / 2.0)), 1.0) * (fs / n)
# freqs = np.arange(0, int(np.ceil((n + 1) / 2.0)), 1.0) * 1
power_spectrums = 20 * np.log10(MagFreq)

# 0dB以上及100-20K Hz
expect_freq = [300, 500, 800, 1000, 2000, 3000, 5000, 7500]
expect_power_spectrum = []
expect_thd = []


def get_square_sum_sqrt(freqs, power_spectrums, target_freqs):
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

                target_ps.append((sums/count) ** 2)
            else:
                target_ps.append(power_spectrums[index] ** 2)

        else:
            target_ps.append(0)


    # target_ps = [power_spectrums[list(freqs).index(freg)]**2 if freg in freqs else 0 for freg in target_freqs]
    # if float("inf") in target_ps:
    #     target_ps
    #     target_ps
    print("target_ps", target_ps)
    target_sum = sum(target_ps)
    print("target_sum", target_sum)

    target_sqrt = math.sqrt(target_sum)
    print("target_sqrt", target_sqrt)

    return target_sqrt


for freg in expect_freq:
    if freg not in freqs:
        raise Exception("{} not in calculation result. Please check log".format(freg))

    index = list(freqs).index(freg)

    # if power_spectrums[index] > 0:
    expect_power_spectrum.append(power_spectrums[index])

    numerator = freg * np.array([2, 3, 4, 5])
    denominator = freg * np.array([1, 2, 3, 4])
    numerator_sum = get_square_sum_sqrt(freqs=freqs, power_spectrums=power_spectrums, target_freqs=numerator)
    denominator_sum = get_square_sum_sqrt(freqs=freqs, power_spectrums=power_spectrums, target_freqs=denominator)

    # thd = ((p2**2 + p3**2 + pn **2 )) ** 0.5 / ((p1**2 + p2**2 + pn **2)) ** 0.5
    thd = 0 if denominator_sum == 0 else (numerator_sum / denominator_sum)
    thd_persents = "{:.3f}%".format(thd if thd != 0 else 0)
    print(thd_persents)

    expect_thd.append(thd_persents)
    # else:
    #     expect_power_spectrum.append(None)
    #     expect_thd.append(None)


# expect_freqAxis = []
# expect_Power_spectrum = []
# for index, freg in enumerate( freqAxis):
#     if 100 < freg and freg < 20000 and Power_spectrum[index] > 0:
#         # print(freg, Power_spectrum[index])
#         expect_freqAxis.append(freg)
#         expect_Power_spectrum.append(Power_spectrum[index])

save_as_csv(expect_freq,
            expect_power_spectrum,
            expect_thd,
            file_path=f'{os.path.dirname(os.path.abspath(__file__))}\\Power_spectrum.csv')

plt.plot(freqs, power_spectrums)  # Power spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power spectrum (dB)')
plt.title(f"{AudioName}")


#Spectrogram

# N = 512  # Number of point in the fft
# f, t, Sxx = signal.spectrogram(Audiodata, fs, window=signal.blackman(N), nfft=N)
# plt.figure()
# plt.pcolormesh(t, f, 20*np.log10(Sxx))  # dB spectrogram
# #plt.pcolormesh(t, f,Sxx) # Lineal spectrogram
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [seg]')
# plt.title('Spectrogram with scipy.signal', size=16)

plt.show()



# sox C:\Users\ryan.jhang\Documents\ryan\note\audio\mix tone 16k 8p.WAV --rate 8000 -n stat -freq  2 >> t.log
