from flask import Flask, render_template, Response
from backend import transit
import json, time, datetime

def formatting(arg1, arg2): 
    information = transit(arg1, arg2)
    f = {
        "station_id": "", 
        "station_name": "",
        "route_id": "",
        "route_emblem": "",
        "terminus": "",
        "time": ""
    }
    f["station_id"] = arg1
    f["station_name"] = information[0]
    f["route_id"] = information[1][1].lower()
    f["route_emblem"] = f"/static/emblems/{information[1][1]}.svg"
    f["terminus"] = information[1][2]
    f["time"] = information[1][0]
    f_file = json.dumps(f)
    return f_file

def currenttime():
    now = (datetime.datetime.now()).strftime("%m/%d/%Y %H:%M")
    return now 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route('/interfaces')
def interfaces():
    def generate():
        value = True
        while (value == True):
            f = {
                "time": ""
            }
            f["time"] = currenttime()
            f_file = json.dumps(f)
            yield "data:" + f_file + "\n\n"
            time.sleep(2)
    return Response(generate(), mimetype= 'text/event-stream')

@app.route('/stationOne')
def stationOne():
    def generate():
        value = True
        while (value == True):
            f_file = formatting("A20", "N")
            yield "data:" + f_file + "\n\n"
            time.sleep(5)
    return Response(generate(), mimetype= 'text/event-stream')

@app.route('/stationTwo')
def stationTwo():
    def generate():
        value = True
        while (value == True):
            f_file = formatting("A20", "S")
            yield "data:" + f_file + "\n\n"
            time.sleep(5)
    return Response(generate(), mimetype= 'text/event-stream')

app.run() 
