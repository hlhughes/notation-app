import subprocess
import sys
import os

if len(sys.argv) != 2:
    print("")
    sys.exit(1)

wav_file_path = sys.argv[1]
# abc_file = sys.argv[2]

# wav_file = "./piano_notes/" + temp + ".wav"

filename = os.path.splitext(os.path.basename(wav_file_path))[0]
print(filename)

# Define the command you want to run
command_1 = "basic-pitch './output' " + wav_file_path
command_2 = "find ./output/" + filename + "_basic_pitch.mid -type f -exec  midi2abc {} -o {}.abc \;"

print(f"./output/{filename}_basic_pitch.mid")
# wav to midi 
result1 = subprocess.run(command_1, shell=True, capture_output=True, text=True)


# midi to abc
result2 = subprocess.run(command_2, shell=True, capture_output=True, text=True)

