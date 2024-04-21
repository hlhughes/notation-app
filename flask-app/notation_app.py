import pyaudio
import wave
import threading
from basic_pitch.inference import predict, Model
from basic_pitch import ICASSP_2022_MODEL_PATH
import os
import global_vars
import time
import serial

mx = threading.Lock()
cv = threading.Condition(mx)

serMx = threading.Lock()

global_vars.recording = False

def readserial(comport, baudrate):
    global serdata

    ser = serial.Serial(comport, baudrate, timeout=None, bytesize=serial.EIGHTBITS, xonxoff=False, rtscts=False, dsrdtr=False)

    while True:
        serMx.acquire()
        serdata = int(ser.readline().decode().strip())
        serMx.release()


def loopaudio_simple():
    
    global serdata
    serdata = 100

    a = threading.Thread(target=readserial, args=('COM5', 115200))
    a.start()
    
    CHUNK = 1024

    # Open Wave File and start play!
    wf = wave.open('drums.wav', 'rb')
    player = pyaudio.PyAudio()

    while global_vars.recording:
        serMx.acquire()
        ratio = serdata / 100
        serMx.release()

        # Open Output Stream (based on PyAudio tutorial)
        stream = player.open(format=player.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=int(ratio*wf.getframerate()),
                            output=True)

        # PLAYBACK LOOP
        data = wf.readframes(CHUNK)
        while data != b'':
            stream.write(data)
            data = wf.readframes(CHUNK)

        wf.rewind()
        stream.close()

def reset():
    print("reset")
    if os.path.exists("temp.mid"):
        os.remove("temp.mid")
    if os.path.exists("temp.wav"):
        os.remove("temp.wav")

    with open(f"./static/realTime.abc", "w") as abc_file:
        pass

def load_model():
    print("load_model")
    return Model(ICASSP_2022_MODEL_PATH)

def predict2abc(model):
    global already_predicted
    print("predict2abc")

    basic_pitch_model = model

    while global_vars.recording: # this should be changed to a condition that checks the user stopped recording
        mx.acquire()
        if (already_predicted):
            cv.wait()

        model_output, midi_data, note_events = predict('temp.wav', basic_pitch_model)
        already_predicted = True
        mx.release()

        midi_data.write('temp.mid')
        # input file, then output file
        print("calling EasyABC's midi2abc.py")
        os.system('python ../EasyABC/midi2abc.py -f temp.mid -o ./static/realTime.abc')

    print("Finished predicting")
        


def record():


    z = threading.Thread(target=loopaudio_simple)
    z.start()

    global already_predicted
    print("record")
    p = pyaudio.PyAudio()

    fs = 44100  # Sample rate
    chunk_size = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2

    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk_size,
                    input=True)
    
    print('Recording')
    frames = []

    while global_vars.recording: # this should be changed to a condition that checks if the user wants to stop recording
        
        for _ in range(0, int(fs / chunk_size * 5)):
            data = stream.read(chunk_size)
            frames.append(data)

        print("Writing wav file")
        
        mx.acquire()
        wf = wave.open("temp.wav", 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

        already_predicted = False
        cv.notify()
        mx.release()


    print('Finished recording')
    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
    loopaudio_simple.exitCond = True


def start(model):
    # create two threads, one for recording, one for converting to abc
    print("start")
    global already_predicted
    already_predicted = True
    x = threading.Thread(target=record)
    y = threading.Thread(target=predict2abc, args=(model,))

    x.start()
    y.start()

    #x.join()
    #y.join()