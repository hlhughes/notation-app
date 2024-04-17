from flask import Flask, render_template, request, url_for, redirect, Response, session
from threading import Thread

import notation_app
import global_vars


model_loaded = False
model = None

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    global model_loaded
    global model
    if request.method == "POST":
        if not model_loaded:
            model = notation_app.load_model()
            model_loaded = True
            
            # Reset sheet music
            

            return render_template("index.html", model_loaded=model_loaded, recording=global_vars.recording)
        else:
            if not global_vars.recording:
                notation_app.reset()
                global_vars.recording = True
                notation_app.start(model)
                print("Start threads somehow")
            else:
                #Somehow stop them
                global_vars.recording = False
                print("Stop threads somehow")
                
            
            return render_template("index.html", model_loaded=model_loaded, recording=global_vars.recording)
    else:
        notation_app.reset()
        return render_template("index.html", model_loaded=model_loaded, recording=global_vars.recording)


if __name__ == "__main__":
    app.run()