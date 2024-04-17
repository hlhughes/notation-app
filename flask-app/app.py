from flask import Flask, render_template, request, url_for, redirect, Response, session
import pyaudio
import realTime
from threading import Thread
import record as record_lib


model_loaded = False
model = None
recording = False

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    global model_loaded
    global model
    global recording
    if request.method == "POST":
        if not model_loaded:
            model = realTime.load_model()
            model_loaded = True
            
            # Reset sheet music
            

            return render_template("index.html", model_loaded=model_loaded, recording=recording)
        else:
            if not recording:

                #Start the multithread stuff here

                realTime.reset()

                p1 = Thread(target=record_lib.record_loop)
                p1.start()
                print("p1, record started")
                
                p2 = Thread(target=realTime.realTimeABC, args=(model,))
                p2.start()
                print("p2, realTime started")

                #p1.join()
                #p2.join()
                #print("processes done")
            else:
                #Somehow stop them
                print("Stop threads somehow")
                
            recording = not recording
            return render_template("index.html", model_loaded=model_loaded, recording=recording)
    else:
        realTime.reset()
        return render_template("index.html", model_loaded=model_loaded, recording=recording)


if __name__ == "__main__":
    app.run()