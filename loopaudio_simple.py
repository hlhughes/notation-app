# Zach Khan, UMich EECS 598
# Last update: 4/17/24
# modified from https://gist.github.com/THeK3nger/3624478


import os
import wave
import threading
import serial
import time


# PyAudio Library
import pyaudio


class WavePlayerLoop(threading.Thread):
    CHUNK = 1024

    def __init__(self, filepath, loop=True):
        """
        Initialize `WavePlayerLoop` class.
        PARAM:
            -- filepath (String) : File Path to wave file.
            -- loop (boolean)    : True if you want loop playback.
                                   False otherwise.
        """
        super(WavePlayerLoop, self).__init__()
        self.filepath = os.path.abspath(filepath)
        self.loop = loop

    def run(self):
        global serdata
        global exitCond
        print("here")

        # Open Wave File and start play!
        wf = wave.open(self.filepath, 'rb')
        player = pyaudio.PyAudio()

        while self.loop:
            ratio = serdata / 100

            # Open Output Stream (based on PyAudio tutorial)
            stream = player.open(format=player.get_format_from_width(wf.getsampwidth()),
                                channels=wf.getnchannels(),
                                rate=int(ratio*wf.getframerate()),
                                output=True)

            # PLAYBACK LOOP
            data = wf.readframes(self.CHUNK)
            while data != b'':
                stream.write(data)
                data = wf.readframes(self.CHUNK)

            wf.rewind()
            stream.close()

            # TODO - choose condition to leave loop
            # TODO - test if external exitCond works
            if(exitCond):
                self.loop = False


        player.terminate()

    def play(self):
        """
        Just another name for self.start()
        """
        self.start()

    def stop(self):
        """
        Stop playback.
        """
        self.loop = False

def readserial(comport, baudrate):
    global serdata
    global lastData

    ser = serial.Serial(comport, baudrate, timeout=None, bytesize=serial.EIGHTBITS, xonxoff=False, rtscts=False, dsrdtr=False)

    while True:
        # Steady State
        if(time.time() - lastData > 10):
            player.loop = False
        else:
            player.loop = True

        serdata = int(ser.readline().decode().strip())
        lastData = time.time()


# Startup
player = WavePlayerLoop("drums.wav", loop=False)
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=None, bytesize=serial.EIGHTBITS, xonxoff=False, rtscts=False, dsrdtr=False)
serdata = int(ser.readline().decode().strip())
serdata = 100
exitCond = False
player.play()
lastData = time.time()

ser = readserial('/dev/ttyACM0', 115200)



    

