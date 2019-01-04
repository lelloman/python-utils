from __future__ import print_function
import wave
import numpy as np
from struct import unpack


class WaveWrap(object):
    def __init__(self, filename, output_window_size, window_overlap, unpack_fmt="<{}h"):
        self.wav_buffer_size = output_window_size - window_overlap
        self.wave_file = wave.open(filename, 'r')
        self.length = self.wave_file.getnframes()
        self.output_window_size = output_window_size
        self.unpack_fmt = unpack_fmt.format(self.wav_buffer_size)

        self.cursor = 1
        self.n_windows = self.length / self.wav_buffer_size

        self.wav_data = np.zeros(self.output_window_size)
        self.fft_input = np.zeros(self.output_window_size)
        self.hamming = np.hamming(self.output_window_size)

    def next_pcm_window(self):
        try:
            wave_data = self.wave_file.readframes(self.wav_buffer_size)
        except Exception as e:
            print(e.message)
            wave_data = np.zeros(self.wav_buffer_size)
        self.cursor += 1
        return unpack(self.unpack_fmt, wave_data)

    def next_fft_input_window(self):
        np.roll(self.wav_data, -self.wav_buffer_size)
        self.wav_data[-self.wav_buffer_size:] = self.next_pcm_window()
        return self.wav_data * self.hamming

    def next_fft_output_window(self):
        fft = np.abs(np.fft.rfft(self.next_fft_input_window()))
        max_energy = max(fft)
        fft /= max_energy
        return fft


window_size = 4096 * 4
overlap = (window_size / 4) * 3

wav_wrap = WaveWrap(filename='bee.wav', output_window_size=window_size, window_overlap=overlap)

bin_size = wav_wrap.wave_file.getframerate() / float(window_size)
print('bin size', bin_size)

d = np.array([wav_wrap.next_fft_output_window() for _ in range(wav_wrap.n_windows)])

print('len(d) = ', len(d))

import matplotlib.pyplot as plt

plt.imshow(np.flip(d.T, 0), interpolation='nearest', aspect='auto')

plt.show()
