import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile

file_path = f'{os.path.dirname(os.path.abspath(__file__))}\\1k_10s.wav'
samplerate, data = scipy.io.wavfile.read(file_path)
# （data = samplerate * t ）
print(data)
print(samplerate)
sample_number = data.shape[0]
print(data.shape)
total_time = int(sample_number / samplerate * 1000)

print(f"total_time{total_time}, sample_number{sample_number}, samplerate{samplerate}, ")

time_series = np.linspace(0, total_time, sample_number)
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(7, 7))
print(time_series)

#data = data[:, 0]
# plot time signal:
axs[0, 0].set_title("Signal")
axs[0, 0].plot(time_series, data, color='C0')
axs[0, 0].set_xlabel("Time (millisecond)")
axs[0, 0].set_ylabel("Amplitude")

n_data = data / np.max(data)
axs[0, 1].set_title("Signal normal")
axs[0, 1].plot(time_series, n_data, color='C0')
axs[0, 1].set_xlabel("Time (millisecond)")
axs[0, 1].set_ylabel("Amplitude")

# plot different spectrum types:
axs[1, 0].set_title("Magnitude Spectrum")
axs[1, 0].magnitude_spectrum(n_data, Fs=samplerate, color='C1')
axs[1, 1].set_title("Log. Magnitude Spectrum")
axs[1, 1].magnitude_spectrum(n_data, Fs=samplerate, scale='dB', color='C1')

axs[2, 0].set_title("Phase Spectrum ")
axs[2, 0].phase_spectrum(n_data, Fs=samplerate, color='C2')

axs[2, 1].set_title("Angle Spectrum")
axs[2, 1].angle_spectrum(n_data, Fs=samplerate, color='C2')
#axs[0, 1].remove()  # don't display empty ax

fig.tight_layout()
plt.show()
