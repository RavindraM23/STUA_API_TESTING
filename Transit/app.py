from flask import Flask, render_template
from rewritecopy import transit
import json 

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
            	yield "data:" + json.load(f_file) + "\n\n"
    return Response(generate(), mimetype= 'text/event-stream')
  

app.run(debug=True) 
