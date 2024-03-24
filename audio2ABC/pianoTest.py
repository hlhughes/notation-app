import numpy as np
from scipy.io.wavfile import read, write
import os

def generate_piano_note(note_freq, duration=1, sampling_rate=44100, volume=0.5):
    """
    Generate a WAV file with a single piano note.
    Args:
    - note_freq (float): Frequency of the note.
    - duration (float): Duration of the note in seconds.
    - sampling_rate (int): Sampling rate for the WAV file.
    - volume (float): Volume of the note (between 0 and 1).
    Returns:
    - numpy array: Array containing the audio data for the note.
    """
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    note = volume * np.sin(2 * np.pi * note_freq * t)
    return note

def save_wav(filename, audio_data, sampling_rate=44100):
    """
    Save audio data as a WAV file.
    Args:
    - filename (str): Name of the output WAV file.
    - audio_data (numpy array): Array containing the audio data.
    - sampling_rate (int): Sampling rate for the WAV file.
    """
    audio_data = np.int16(audio_data * 32767)
    write(filename, sampling_rate, audio_data)

# Ensure the output directory exists
output_dir = "piano_notes"
os.makedirs(output_dir, exist_ok=True)

# List of piano notes (frequency, note name)
piano_notes = [
    (261.63, "C4"),  # C4
    (293.66, "D4"),  # D4
    (329.63, "E4"),  # E4
    (349.23, "F4"),  # F4
    (392.00, "G4"),  # G4
    (440.00, "A4"),  # A4
    (493.88, "B4"),  # B4
    (523.25, "C5"),  # C5
]

# Generate and save each piano note
for note_freq, note_name in piano_notes:
    note_data = generate_piano_note(note_freq)
    save_wav(os.path.join(output_dir, f"{note_name}.wav"), note_data)

def combine_wav_files(input_files, output_file):
    """
    Combine multiple WAV files into a single WAV file.
    Args:
    - input_files (list of str): List of input WAV file paths.
    - output_file (str): Output WAV file path for the combined audio.
    """
    combined_audio = []
    for file in input_files:
        rate, data = read(file)
        combined_audio.extend(data)
    combined_audio = np.array(combined_audio)
    write(output_file, rate, combined_audio)

# List of input WAV files (add more as needed)
input_files = [os.path.join(output_dir, f"{note_name}.wav") for _, note_name in piano_notes]

# Output WAV file
output_file = os.path.join(output_dir, "combined_piano_notes.wav")

# Combine WAV files
combine_wav_files(input_files, output_file)
