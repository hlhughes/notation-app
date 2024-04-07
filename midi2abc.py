import sys
import pretty_midi
import os
import time

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
    bpm = int(midi_data.estimate_tempo())
    tempo = f"1/4={bpm}"
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
            # note_str += f"{pretty_midi.note_number_to_name(note.pitch)} " #{int(note.start*1000)}{int(note.end*1000)}
            note_str += f"{pitchToAbc(note)}"

            note_rhythm = convertRhythm(note)
            if note_rhythm != "null":
                note_str += note_rhythm

            note_str += " "

            note_info = ""
            note_info += f"Pitch: {note.pitch}\n"
            note_info += f"Start: {note.start}s\n"
            note_info += f"Duration: {note.end - note.start}s\n"
            note_info += f"Computed abc: {pitchToAbc(note)}\n"
            note_info += f"Computed Duration: {convertRhythm(note)}\n"
            note_info += "--------\n"
            #print(note_info)


        
        # End the current voice
        note_str += "| "
    
    return note_str

def pitchToAbc(note):
    Notes = ["C", "^D", "D", "^E", "E", "F", "^G", "G", "^A", "A", "^B", "B"]
    note_name = Notes[note.pitch % len(Notes)]

    if 72 <= note.pitch <= 83:
        note_name = note_name.lower()

    if (note.pitch >= 84):
        octaves = int(note.pitch / len(Notes)) - 6
        for i in range(octaves):
            note_name += "'"
    elif (note.pitch <= 59):
        octaves = abs(int(note.pitch / len(Notes)) - 5)
        for i in range(octaves):
            note_name += ","
    return note_name

def convertRhythm(note):
    global bpm
    bpm = 160
    duration = note.end - note.start
    unitDurationSeconds = 60.0 / bpm
    Durations = [0, unitDurationSeconds / 2.0, unitDurationSeconds, unitDurationSeconds * 2.0, unitDurationSeconds * 4.0]
    closest_duration = min(Durations, key=lambda x:abs(x-duration)) 

    if closest_duration == 0:
        return "null"
    #elif closest_duration == unitDurationSeconds / 4.0:
        #return "/4"
    elif closest_duration == unitDurationSeconds / 2.0:
        return "/2"
    elif closest_duration == unitDurationSeconds:
        return ""
    elif closest_duration == unitDurationSeconds * 2.0:
        return "2"
    elif closest_duration == unitDurationSeconds * 4.0:
        return "4"

def update_abc(midi_data):
    abc_data = "" 
    abc_data = get_abc_metadata(midi_data)
    abc_data += get_abc_notes(midi_data)

    with open(f"./output/realTime.abc", "w") as abc_file:
        abc_file.write(abc_data)