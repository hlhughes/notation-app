import sys
import pretty_midi
import os
import time

import tensorflow as tf

from basic_pitch.inference import predict, Model
from basic_pitch import ICASSP_2022_MODEL_PATH

def concatenate_midi(new_midi):
    
    accumulated_time = curr_midi.get_end_time()

    # For each instrument in the MIDI file
    for instrument in new_midi.instruments:
        inst_key = (instrument.program, instrument.is_drum)
        
        # If we've already created an instrument for this program number, retrieve it
        if inst_key in program_to_instrument:
            merged_instrument = program_to_instrument[inst_key]
        else:
            # Otherwise, create a new instrument and add to the dictionary
            merged_instrument = pretty_midi.Instrument(program=instrument.program, is_drum=instrument.is_drum)
            program_to_instrument[inst_key] = merged_instrument
            # Also, add the instrument to the merged MIDI object
            curr_midi.instruments.append(merged_instrument)

        # Adjust and append all notes from the current instrument to the merged instrument
        for note in instrument.notes:
            # Create a copy of the note to avoid modifying the original
            copied_note = pretty_midi.Note(
                velocity=note.velocity, 
                pitch=note.pitch, 
                start=note.start + accumulated_time, 
                end=note.end + accumulated_time
            )
            merged_instrument.notes.append(copied_note)

        # Adjust and append pitch bends
        for pitch_bend in instrument.pitch_bends:
            copied_pitch_bend = pretty_midi.PitchBend(
                pitch=pitch_bend.pitch, 
                time=pitch_bend.time + accumulated_time
            )
            merged_instrument.pitch_bends.append(copied_pitch_bend)

        # Adjust and append control changes
        for control_change in instrument.control_changes:
            copied_control_change = pretty_midi.ControlChange(
                number=control_change.number, 
                value=control_change.value, 
                time=control_change.time + accumulated_time
            )
            merged_instrument.control_changes.append(copied_control_change)

def get_abc(midi_data):
    abc_text = get_abc_metadata(midi_data)
    abc_text += get_abc_notes(midi_data)
    return abc_text


def get_abc_metadata(midi_data):
    abc_metadata_text = ""
    
    # Set the tune index (X)
    abc_metadata_text += "X: 1\n"
    
    # Set the title (T)
    abc_metadata_text += f"T: Real Time Sheet Music\n"
    
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

def update_abc(wav_file_path, first):
    abc_data = "" 

    model_output, midi_data, note_events = predict(
        wav_file_path,
        basic_pitch_model,
    )

    filename = os.path.splitext(os.path.basename(wav_file_path))[0]
    if (first):
        global curr_midi
        curr_midi = midi_data
    else:
        concatenate_midi(midi_data)

    abc_data += get_abc(midi_data)

    with open(f"./output/realTime.abc", "w") as abc_file:
        abc_file.write(abc_data)

def realTimeABC():
    idx = 1
    print("realTimeABC started")
    global basic_pitch_model
    basic_pitch_model = Model(ICASSP_2022_MODEL_PATH)
    global program_to_instrument
    program_to_instrument = {}
    wav_file_dir = f"./piano_notes"

    while True:
        print(f"Running sample_{idx}.wav")
        file_path = f"{wav_file_dir}/sample_{idx}.wav"

        while not os.path.exists(file_path):
            print("sleep")
            time.sleep(3)

        print("wake up")
        # now sample_idx.wav exist
        if idx == 1:
            update_abc(file_path, True)
        else:
            update_abc(file_path, False)

        idx += 1
        time.sleep(2) # might need to change the duration