from ast import arg
from flask import Flask, render_template, Response
import stua
import json, time, datetime

stua.keySubway("p4G33OQzU8acTdI6FbwCQ3C4bXKbmLFla5ZSDvdc")
cycle = (("M21", "S"), ("640", "S"), ("137", "S"), ("A36", "S"))

def formatting(arg1, arg2):
    f = {
        "station": "",
        "train1": {
            "route_id": "",
            "terminus": "",
            "terminus_id": "",
            "station": "",
            "station_id": "",
            "direction": "",
            "time": "",
            "service_pattern": "",
            "service_description": "",
            "trip_id": "",
            "route_emblem": ""
        },
        "train2": {
            "route_id": "",
            "terminus": "",
            "terminus_id": "",
            "station": "",
            "station_id": "",
            "direction": "",
            "time": "",
            "service_pattern": "",
            "service_description": "",
            "trip_id": "",
            "route_emblem": ""
        },
        "train3": {
            "route_id": "",
            "terminus": "",
            "terminus_id": "",
            "station": "",
            "station_id": "",
            "direction": "",
            "time": "",
            "service_pattern": "",
            "service_description": "",
            "trip_id": "",
            "route_emblem": ""
        },
        "train4": {
            "route_id": "",
            "terminus": "",
            "terminus_id": "",
            "station": "",
            "station_id": "",
            "direction": "",
            "time": "",
            "service_pattern": "",
            "service_description": "",
            "trip_id": "",
            "route_emblem": ""
        }
    }
    integer = 4
    while (integer > 0):
        information = stua.gtfsSubway()
        information.get(arg1, arg2,integer)
        f["station"] = stua.convertSubway(arg1) + f" ({arg2})"
        f[f"train{integer}"]["route_id"] = information.route_id
        f[f"train{integer}"]["terminus"] = information.terminus
        f[f"train{integer}"]["terminus_id"] = information.terminus_id
        f[f"train{integer}"]["station"] = information.station
        f[f"train{integer}"]["station_id"] = information.station_id
        f[f"train{integer}"]["direction"] = information.direction
        f[f"train{integer}"]["time"] = information.time
        f[f"train{integer}"]["service_pattern"] = information.service_pattern
        f[f"train{integer}"]["service_description"] = information.service_description
        f[f"train{integer}"]["trip_id"] = information.trip_id
        f[f"train{integer}"]["route_emblem"] = f"/static/emblems/{(information.route_id).lower()}.svg"
        integer -= 1
    f_file = json.dumps(f)
    return f_file

def currenttime():
    now = (datetime.datetime.now()).strftime("%m/%d/%Y %H:%M")
    return now 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("screenwidth.html")

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

@app.route('/info')
def info():
    def generate():
        global cycle
        start = 0
        after = (datetime.datetime.now() + datetime.timedelta(minutes=1))
        value = True
        while (value == True):
            before = datetime.datetime.now()
            print(before.strftime("%H:%M"))
            print(after.strftime("%H:%M"))
            if (before).strftime("%H:%M") == (after).strftime("%H:%M"):
                start += 1
                after = before + datetime.timedelta(minutes=1)
                if (start == len(cycle)):
                    start = 0
            f_file = formatting(cycle[start][0], cycle[start][1])
            print(start)
            yield "data:" + f_file + "\n\n"
            time.sleep(5)
    return Response(generate(), mimetype= 'text/event-stream')

app.run() 
