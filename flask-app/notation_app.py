import pyaudio
import wave
import threading
from basic_pitch.inference import predict, Model
from basic_pitch import ICASSP_2022_MODEL_PATH
import os
import global_vars

mx = threading.Lock()
cv = threading.Condition(mx)

global_vars.recording = False


def reset():
    if os.path.exists("temp.mid"):
        os.remove("temp.mid")
    if os.path.exists("temp.wav"):
        os.remove("temp.wav")

    with open(f"./static/realTime.abc", "w") as abc_file:
        pass

def load_model():
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
        os.system('python ../EasyABC/midi2abc.py -f temp.mid -o ./static/realTime.abc')
        


def record():
    global already_predicted
    print("record")
    i = 0
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
        
        for j in range(0, int(fs / chunk_size * 5)):
            data = stream.read(chunk_size)
            frames.append(data)

        wav_filename = "temp.wav"

        print(f"Writing to {wav_filename}")
        
        mx.acquire()

        wf = wave.open(wav_filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

        already_predicted = False
        cv.notify()
        mx.release()

        i += 1  # Increment the counter for the next filename

    print('Finished recording')
    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()


def start(model):
    # create two threads, one for recording, one for converting to abc
    print("main")
    global already_predicted
    already_predicted = True
    x = threading.Thread(target=record)
    y = threading.Thread(target=predict2abc, args=(model,))

    x.start()
    y.start()

    #x.join()
    #y.join()

if __name__ == '__main__':
    main()