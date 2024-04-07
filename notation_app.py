import pyaudio
import wave
import threading
from basic_pitch.inference import predict, Model
from basic_pitch import ICASSP_2022_MODEL_PATH
import time

from midi2abc import update_abc

mx = threading.Lock()
cv = threading.Condition(mx)
already_predicted = True

def predict2abc():
    print("predict2abc")

    basic_pitch_model = Model(ICASSP_2022_MODEL_PATH)
    while True: # this should be changed to a condition that checks the user stopped recording
        mx.acquire()
        if (already_predicted):
            cv.wait()

        model_output, midi_data, note_events = predict('temp.wav', basic_pitch_model)
        mx.release()
    
        # here do midi 2 abc & update abc file that is displayed on the webpage
        update_abc(midi_data)


def record():
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

    while i < 5: # this should be changed to a condition that checks if the user wants to stop recording
        
        for j in range(0, int(fs / chunk_size * 5)):
            data = stream.read(chunk_size)
            frames.append(data)

        #wav_filename = f"./piano_notes/sample_{i}.wav"
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


def main():
    # create two threads, one for recording, one for converting to abc
    print("main")
    
    x = threading.Thread(target=record)
    y = threading.Thread(target=predict2abc)

    x.start()
    y.start()

    x.join()
    y.join()

if __name__ == '__main__':
    main()