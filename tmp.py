import pyaudio
import wave
import threading
from basic_pitch.inference import predict, Model
from basic_pitch import ICASSP_2022_MODEL_PATH
import os

x, midi_data, y = predict('gymnopedie-n1-200688.mp3', Model(ICASSP_2022_MODEL_PATH))

midi_data.write('EasyABC/temp.mid')
os.system('python EasyABC/midi2abc.py -f EasyABC/temp.mid -o EasyABC/temp.abc')