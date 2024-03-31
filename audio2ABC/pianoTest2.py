import numpy as np
import scipy.io.wavfile as wavfile

# Define parameters
duration = 3  # Duration of the WAV file in seconds
sample_rate = 44100  # Sample rate (samples per second)
freq_d = 293.66  # Frequency of note D (in Hz)
freq_e = 329.63  # Frequency of note E (in Hz)

# Generate time array
t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)

# Generate waveforms for notes D and E
waveform_d = np.sin(2 * np.pi * freq_d * t)
waveform_e = np.sin(2 * np.pi * freq_e * t)

# Mix the waveforms
waveform_mix = 0.5 * waveform_d + 0.5 * waveform_e

# Normalize to 16-bit range
waveform_mix *= 32767 / np.max(np.abs(waveform_mix))

# Convert to 16-bit integers
waveform_mix = waveform_mix.astype(np.int16)

# Save as WAV file
wavfile.write('./piano_notes/DE.wav', sample_rate, waveform_mix)
