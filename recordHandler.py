import time
import sys
import pyaudio
import wave
import numpy as np
import scipy.signal as signal
import datetime
from funcs import setDevice, callback_withDSP,nonblocking,blocking,getformat,getRate


#Predefine default values
WIDTH = 2
CHANNELS = 1
RATE = 44100
CHUNK = 1024
DURATION = 5
FORMAT = pyaudio.paInt16
INPUT_DEVICE = 14
OUPUT_DEVICE = 0

# Get input from command line
if(sys.argv[1] != ''): RATE = getRate(sys.argv[1])
if(sys.argv[2] != ''): CHANNELS = int(sys.argv[2])
if(sys.argv[3] != ''): FORMAT = getformat(sys.argv[3])

# Select Input and Output Devices
INPUT_DEVICE,OUPUT_DEVICE =setDevice()


print("\n\n\n ==================================================== ")

# method selection
val = input("Which method of recording do you want?\n1.NoBlocking\n2.Blocking\nPress the number of the method:")

if(val == "1"):
	nonblocking(CHANNELS,FORMAT,RATE,DURATION,INPUT_DEVICE,OUPUT_DEVICE)
elif(val == "2"):
	blocking(CHANNELS,FORMAT,RATE,CHUNK,DURATION,INPUT_DEVICE,OUPUT_DEVICE)
else:
	print("Undefined method!")

print("\n")

