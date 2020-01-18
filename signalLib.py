import pyaudio
import time
import numpy as np
import scipy.signal as signal
import wave
import datetime
import librosa

def low_pass_filt(s, fL=0.2, N=59):
    h = np.sinc(2 * fL * (np.arange(N) - (N - 1) / 2))
    h *= np.blackman(N)
    h /= np.sum(h)
    s = np.convolve(s, h)
    return s


def high_pass_filt(s, fH, N):
    h = np.sinc(2 * fH * (np.arange(N) - (N - 1) / 2))
    h *= np.blackman(N)
    h /= np.sum(h)
    h = -h
    h[(N - 1) // 2] += 1
    s = np.convolve(s, h)
    return s


def bandpass_filt(s, fH, fL, N):
    # low-pass filter with fH.
    h = np.sinc(2 * fH * (np.arange(N) - (N - 1) / 2))
    h *= np.blackman(N)
    h /= np.sum(h)
    # high-pass filter with fL.
    hh = np.sinc(2 * fL * (np.arange(N) - (N - 1) / 2))
    hh *= np.blackman(N)
    hh /= np.sum(h)
    hh = -h
    hh[(N - 1) // 2] += 1
    final = np.convolve(h, hh)
    np.convolve(s, final)
    return s

def bandreject_filt(s, fH, fL, N):
    n = np.arange(N)
   # low-pass filter with fH.
    h = np.sinc(2 * fL * (np.arange(N) - (N - 1) / 2))
    h *= np.blackman(N)
    h /= np.sum(h)
    # high-pass filter with fL.
    hh = np.sinc(2 * fH * (np.arange(N) - (N - 1) / 2))
    hh *= np.blackman(N)
    hh /= np.sum(h)
    hh = -h
    hh[(N - 1) // 2] += 1
    # Add both filters.
    final = h + hh
    np.convolve(s, final)
    return s
# zero_crossing_rate function from librosa library
def zcr(y):
    s = librosa.feature.zero_crossing_rate(y = y)
    return s
# Root mean square function from librosa library
def rms(y):
    s = librosa.feature.rms(S = y,frame_length = 2047) #in librosa > 0.7 rmse (for each frame) insert in to rms
    return s


