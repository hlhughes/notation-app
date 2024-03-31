import sys
import pretty_midi
import os


import tensorflow as tf

from basic_pitch.inference import predict, Model
from basic_pitch import ICASSP_2022_MODEL_PATH

if len(sys.argv) != 2:
    print("Please RUN: python converter.py <input wav file path>")
    sys.exit(1)

wav_file_dir = sys.argv[1]

basic_pitch_model = Model(ICASSP_2022_MODEL_PATH)

input_file_list = ['combined_piano_notes.wav', 'combined.wav']

abc_data = "" 

#----------------------------------------------------------------------------------


def get_abc_metadata(midi_data, filename):
    abc_metadata_text = ""
    
    # Set the tune index (X)
    abc_metadata_text += "X: 1\n"
    
    # Set the title (T)
    abc_metadata_text += f"T: from {filename}\n"
    
    # Set the time signature (M)
    abc_metadata_text += "M: 4/4\n"
    
    # Set the default note length (L)
    abc_metadata_text += "L: 1/8\n"
    
    # Set the tempo (Q)
    tempo = f"1/4={int(midi_data.estimate_tempo() * 2)}"
    abc_metadata_text += f"Q: {tempo}\n"
    
    # Set the key signature (K)
    abc_metadata_text += "K: C % 0 sharps\n"

    abc_metadata_text += "V: 1\n"
    
    return abc_metadata_text

def get_abc_notes(midi_data):
    note_str = ""
    for instrument in midi_data.instruments:
        
        # Iterate through each note in the instrument
        for note in instrument.notes:
            # Format the note information in ABC format and append to the ABC data
            note_str += f"{pretty_midi.note_number_to_name(note.pitch)} " #{int(note.start*1000)}{int(note.end*1000)}
        
        # End the current voice
        note_str += "| "
    
    return note_str

for i in range(len(input_file_list)):
    wav_file_path = f"{wav_file_dir}/{input_file_list[i]}"
    model_output, midi_data, note_events = predict(
        wav_file_path,
        basic_pitch_model,
    )

    filename = os.path.splitext(os.path.basename(input_file_list[i]))[0]
    if(i == 0):
        abc_data = get_abc_metadata(midi_data, filename)

    abc_data += get_abc_notes(midi_data)

    with open("./output/output.abc", "w") as abc_file:
        abc_file.write(abc_data)
