from flask import Flask, render_template, Response
from rewritecopy import transit
import json 
import time 

app = Flask(__name__)

@app.route("/") 
def index():
    return render_template('index.html')
    
@app.route('/stations')
def stations():
    def generate():
        value = True
        while (value == True):
            with open("export.json","r") as f:
                f_file = json.load(f)
                f_file = json.dumps(f_file)
                yield "data:" + f_file + "\n\n"
                time.sleep(5)
    return Response(generate(), mimetype= 'text/event-stream')
  

app.run(debug=True) 
