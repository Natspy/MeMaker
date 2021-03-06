# -*- coding: utf-8 -*-
"""prototyp_signal_pipeline.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZrAk-S8bnZRy0LE14qyzuNdzGXqA4TGp
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from  scipy.signal import iirnotch
from  scipy.signal import butter
from  scipy.signal import lfilter, filtfilt
import re
import os

plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['figure.dpi'] = 100 

def pipeline(path: str):
  with open(path+'\\'+'BitalinoECG.txt', 'r') as f:
    s = np.zeros(len(f.readlines()))
    times =[]
    f.seek(0)
    i = 0
    for line in f.readlines():
      values = line.split('\t')
      s[i] = np.double(values[0])
      time = int(values[1][:2])*3600+int(values[1][2:4])*60+int(values[1][4:6])+int(values[1][7:])*0.001
      times.append(time)
      i += 1

  with open(path+'\\'+'Triggers.txt', 'r') as f:
    timestamps = []
    for line in f.readlines()[1:17]:
      values = line.split('\t')
      timestamps.append((int(values[1][:2])*3600+int(values[1][2:4])*60+int(values[1][4:6])-int(times[0]), int(values[2][:2])*3600+int(values[2][2:4])*60+int(values[2][4:6])-int(times[0])))
 
  with open(path+'\\'+'BitalinoGSR.txt', 'r') as f:
    g = np.zeros(len(f.readlines()))
    f.seek(0)
    i = 0
    for line in f.readlines():
      values = line.split('\t')
      g[i] = np.double(values[0])
      i += 1

  Fs = 100
  T = len(s)/Fs
  dt = 1/Fs
  t = np.arange(0,T,dt)

  Tags = np.zeros(96000)
  for item in timestamps:
    idx0 = int(item[0]*Fs)
    idx1 = int(item[1]*Fs)
    Tags[idx0:idx1] = 1

  [b1,a1] = butter(1,0.6,fs=Fs,btype='highpass')
  sf1 = filtfilt(b1, a1, s)
  [b2,a2] = iirnotch(50, 30, fs=Fs)
  sf2 = filtfilt(b2, a2, sf1)
  [b3,a3] = butter(2,40,fs=Fs,btype='lowpass')
  sf = filtfilt(b3, a3, sf2)

  #plt.plot(t[34000:35000],sf[34000:35000])
  #plt.plot(t[34000:35000],Tags[34000:35000])

  wynik = [sf[:6000], sf[6000:102000], Tags, t, g[:6000], g[6000:102000], times]
  return wynik

folder = r'D:\GitHub\Neurohackator2021TeamLutraLutra\electrocardiogram-skin-conductance-and-respiration-from-spider-fearful-individuals-watching-spider-video-clips-1.0.0'

subfolders = [f.path for f in os.scandir(folder) if f.is_dir()]

EcgSet = {}
user = 0
for path in subfolders:
  EcgSet[user] = pipeline(path)
  user += 1

import pickle

ECG_file = open("ECG_data.pkl", "wb")
pickle.dump(EcgSet, ECG_file)
ECG_file.close()

ECG_file = open("ECG_data.pkl", "rb")
output = pickle.load(ECG_file)
print(output)
ECG_file.close()