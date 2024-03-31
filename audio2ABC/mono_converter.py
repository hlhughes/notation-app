### aubio can only find the most dominant note, so no multi note at the same time

import aubio
import numpy as np
import sys

def wav_to_abc(wav_file, abc_file):
    # Parameters for pitch detection
    samplerate, win_s, hop_s = 44100, 1024, 512
    aubio_source = aubio.source(wav_file, samplerate, hop_s)
    samplerate = aubio_source.samplerate
    pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(0.8)

    notes = []
    previous_pitch = 0
    # Read and analyze audio file
    while True:
        samples, read = aubio_source()
        pitch = pitch_o(samples)[0]

        # Consider a note change if the pitch changes significantly (more than 1 MIDI note)
        if abs(pitch - previous_pitch) > 1:
            print(f"pitch = {pitch}")
            midi_note = int(pitch)
            note = midi_to_abc(midi_note)
            print(f"abc note = {note}")
            if note:  # If a valid note is detected
                notes.append(note)
            previous_pitch = pitch
        if read < hop_s: break

    # Write notes to ABC file
    notes_sequence = " ".join(notes)
    with open(abc_file, 'w') as f:
        f.write(f"X:1\nT:Extracted Melody\nM:4/4\nL:1/4\nK:C\n{notes_sequence}\n")


def midi_to_abc(midi_note):
    # Map MIDI note numbers to ABC notation
    print(f"midi note = {midi_note}")
    # notes = "C D E F G A B".split()
    note_names = ["C", "_D", "D", "_E", "E", "F", "_G", "G", "_A", "A", "_B", "B"]
    note_index = midi_note % len(note_names)
    octave = midi_note // 12 - 5  # MIDI octave 5 is considered octave 0 in ABC
    abc_note = note_names[note_index] + (octave * "'")
    return abc_note

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py input_wav_file output_abc_file")
        sys.exit(1)

    wav_file = sys.argv[1]
    abc_file = sys.argv[2]

    wav_to_abc(f"./piano_notes/{wav_file}", abc_file)
