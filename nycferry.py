from decimal import InvalidContext
import requests, csv, datetime, math, os, json, calendar
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
import gtfs_realtime_pb2, nyct_subway_pb2
from stua import convertFerry as convertFerry

def _transitFerry(stop, responses):
    current_time = datetime.datetime.now()
    times = []
    destination = []
    #print(API)
    response = requests.get("http://nycferry.connexionz.net/rtt/public/utility/gtfsrealtime.aspx/tripupdate")
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    with open(f"logs/NYCFerry/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","w") as test:
        test.write(str(feed)+ f" {datetime.datetime.now()}\n")
    for entity in feed.entity:
        for update in entity.trip_update.stop_time_update:
            #print(update.stop_id)
            if (update.stop_id == stop):
                #print("checkpointA")
                trip_id = entity.trip_update.trip.trip_id

                for boat in entity.trip_update.trip:
                    if (boat.trip_id == trip_id):
                        times.append(entity.trip_update.stop_time_update.stop_id)
                break
                
                #print(data["gtfs"]["stops"])
                #for i in data["gtfs"]["stops"]:
                #print(i["stop_id"] + " " + i["stop_name"])
    
    return times

e = _transitFerry("88", 1)
print(e)