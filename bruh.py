from basic_pitch.inference import predict, Model
from basic_pitch import ICASSP_2022_MODEL_PATH
from midi2abc import midi2abc

basic_pitch_model = Model(ICASSP_2022_MODEL_PATH)

# ultimately, this will be wrapped in a flask app so that the user can easily interact with it

recording = True # user will set this via button on page

while(recording):

    # record audio from laptop mic

    model_output, midi_data, note_events = predict('input.mp3', basic_pitch_model)
    # midi_data is type <class 'pretty_midi.pretty_midi.PrettyMIDI'>
    # https://craffel.github.io/pretty-midi/#pretty-midi-prettymidi
    # https://github.com/craffel/pretty-midi
    # https://github.com/craffel/pretty-midi/blob/main/Tutorial.ipynb


    # 1. use midi2abc w/ the newly predicted midi_data
    # 2. concatenate the curr abc notation with the old abc notation
    
    # 3. display the abc notation on the webpage, and run the cycle again until user stops recording
    # we will have to make sure that once the user stops recording, the remaining data is still processed