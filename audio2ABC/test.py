from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH

model_output, midi_data, note_events = predict("./piano_notes/CD.wav", ICASSP_2022_MODEL_PATH)