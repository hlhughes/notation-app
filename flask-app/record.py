import pyaudio
import wave
import time

def record_audio(wav_filename, record_seconds=5, chunk_size=1024, sample_format=pyaudio.paInt16, channels=1, fs=44100):
    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print(f'Recording {wav_filename}')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk_size,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 5 seconds
    for _ in range(0, int(fs / chunk_size * record_seconds)):
        data = stream.read(chunk_size)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(wav_filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


def record_loop():
    print("record_loop started")
    i = 1  # Initialize the counter for the filename
    while i < 5:
        filename = f"./audio_files/sample_{i}.wav"
        record_audio(filename)
        i += 1  # Increment the counter for the next filename
