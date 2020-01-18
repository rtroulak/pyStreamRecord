import time
import sys
import pyaudio
import wave
import numpy as np
import scipy.signal as signal
import datetime
from signalLib import low_pass_filt, high_pass_filt,bandpass_filt,bandreject_filt,zcr,rms

p = pyaudio.PyAudio()
b,a=signal.iirdesign(0.03,0.07,5,40)
fulldata = np.array([])


# Callback Function with filters in comments
def callback_withDSP(in_data, frame_count, time_info, flag):
    global b,a,fulldata
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    type(audio_data)
    # Choose the filtering of audio data
    # audio_data = signal.filtfilt(b,a,audio_data,padlen=200).astype(np.int16).tostring()
    # audio_data = low_pass_filt(audio_data, fL=0.2, N=59).astype(np.int16).tostring()
    # audio_data = high_pass_filt(audio_data, fH=0.2, N=59).astype(np.int16).tostring()
    audio_data = bandreject_filt(audio_data, fH=0.4, fL=0.1, N=59).astype(np.int16).tostring() #put filter
    # audio_data = bandpass_filt(audio_data, fH=0.4, fL=0.1, N=59).astype(np.int16).tostring() #put filter
    # audio_data = zcr(y = audio_data) #put ZCR
    # audio_data = rms(y = audio_data) #put ZCR
    fulldata = np.append(fulldata,audio_data) 
    print('non-blocking mode | ',datetime.datetime.now(), end='\r', flush=True)
    return (audio_data, pyaudio.paContinue)

# Function with the implementation of non-blocking mode recording
def nonblocking(channelsIn,formatIn,rateIn,duration,input_device_index,output_device_index):
	# open stream
	stream = p.open(format=formatIn,
	                channels=channelsIn,
	                rate=rateIn,
	                output=True,
	                input=True,
	                stream_callback=callback_withDSP,input_device_index = input_device_index,output_device_index = output_device_index)
	stream.start_stream()
	import os
	os.system('clear') 
	print("Recording In Proccess for ",duration,"sec...")
	# recording in rpoccess
	while stream.is_active():
	    time.sleep(duration)
	    stream.stop_stream()
	stream.close()# stop stream

	p.terminate()
	print("\nDone!")

	# file creation
	output = wave.open("non-blocking.wav",'w')
	output.setparams((channelsIn, 2, rateIn, 0, 'NONE', 'compressed')) 
	output.writeframes(fulldata)
	output.close()

# Function with the implementation of blocking mode recording
def blocking(channelsIn,formatIn,rateIn,chunckIn,duration,input_device_index,output_device_index):
	# open stream
	stream = p.open(format=formatIn, channels=channelsIn,
	                rate=rateIn, input=True,output=True,
	                frames_per_buffer=chunckIn,input_device_index = input_device_index,output_device_index = output_device_index)
	stream.start_stream()
	print("Recording In Proccess for ",duration,"sec...")
	frames = []
	# recording in Proccess
	for i in range(0, int(rateIn / chunckIn * duration)):
	    data = stream.read(chunckIn)
	    frames.append(data)
	    print('blocking mode | ',datetime.datetime.now(), end='\r', flush=True)
	# stop stream
	stream.stop_stream()
	stream.close()
	p.terminate()
	print("\nDone!")
	
	# file creation
	waveFile = wave.open("blocking.wav", 'wb')
	waveFile.setnchannels(channelsIn)
	waveFile.setsampwidth(p.get_sample_size(formatIn))
	waveFile.setframerate(rateIn)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()



# Function to show the avaliable input and output
def setDevice():
	audio = pyaudio.PyAudio()
	info = audio.get_host_api_info_by_index(0)
	numdevices = info.get('deviceCount')
	INPUT_DEVICE = 14
	OUPUT_DEVICE = 0

	print("\n\n\n ==================================================== ")
	print("\nList of Devices:")
	# prin the list of inut and output devices
	for i in range (0,numdevices):
       		if audio.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
            		print ( i, " - ", audio.get_device_info_by_host_api_device_index(0,i).get('name'),"[Input]")

       		if audio.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
                	print ( i, " - ", audio.get_device_info_by_host_api_device_index(0,i).get('name'),"[Output]")

	devinfo = audio.get_device_info_by_index(1)
	print ("Selected device is ",devinfo.get('name'))


	input_device = input("\nGive Input Device ID(press Enter for default):")
	output_device = input("\nGive Output Device ID(press Enter for default):")
	if(input_device != ''): INPUT_DEVICE = int(input_device)
	if(output_device != ''): OUPUT_DEVICE = int(output_device)
	return INPUT_DEVICE,OUPUT_DEVICE


# Fucntion to set the sample format
def getformat(format):
	# paFloat32, paInt32, paInt24, paInt16, paInt8, paUInt8, paCustomFormat 
	if(format == 'paFloat32'):
		return pyaudio.paFloat32
	elif(format == 'paInt24'):
		return pyaudio.paInt24
	elif(format == 'paInt16'):
		return pyaudio.paInt16
	elif(format == 'paInt32'):
		return pyaudio.paInt32
	elif(format == 'paInt8'):
		return pyaudio.paInt8
	elif(format == 'paUInt8'):
		return pyaudio.paUInt8
	elif(format == 'paCustomFormat'):
		return pyaudio.paCustomFormat
	else:
		print("\n\n*** INPUT ERROR MESSAGE ***\nNot valid sample format. Array of valid sample formats(paFloat32, paInt32, paInt24, paInt16, paInt8, paUInt8, paCustomFormat)\n***")
		exit()

# Fucntion to set the sample format
def getRate(srate):
	rate = int(srate)
	samplerates = [8000,11025,16000,22050,32000,37800,44056,44100,47250,48000,50000,50400,64000,88200,96000,176400,192000,352800,2822400,5644800,11289600,22579200]
	if rate in samplerates:
		return int(rate);
	else:
		print("\n\n*** INPUT ERROR MESSAGE ***\nNot valid Sample Rate. Array of valid sample rates (8000,11025,16000,22050,32000,37800,44056,44100,47250,48000,50000,50400,64000,88200,96000,176400,192000,352800,2822400,5644800,11289600,22579200)\n***")
		exit()