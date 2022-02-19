import requests, csv, datetime, math, os, json
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
import gtfs_realtime_pb2, nyct_subway_pb2

APISubway = ""
APIBus = ""
APILIRR = ""
APIMNR = "" 
#6f064d4d-ed7d-415a-9d4a-c01204897506
#p4G33OQzU8acTdI6FbwCQ3C4bXKbmLFla5ZSDvdc

class gtfs(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def set(self):
        pass

    @abstractmethod
    def get(self):
        pass

class gtfsSubway(gtfs):
    def __init__(self):
        self.route_id = ""
        self.terminus = ""
        self.terminus_id = ""
        self.station = "" 
        self.station_id = ""
        self.direction = ""
        self.time = 0
        self.service_pattern = ""
        self.service_description = ""
        self.trip_id = ""

    def set(self, route_id, terminus_id, station_id, direction, time, pattern, description, trip_id):
        self.route_id = route_id
        self.terminus = convertSubway(terminus_id)
        self.terminus_id = terminus_id
        self.station = convertSubway(station_id)
        self.station_id = station_id
        self.direction = direction
        self.time = time
        self.service_pattern = pattern
        self.service_description = description
        self.trip_id = trip_id

    def get(self, station, direction, responses):
        _validkeySubway(_getAPISubway())
        output = _transitSubway(station, direction, responses, _getAPISubway())
        if (output == "NO TRAINS"):
            self.route_id = "NO TRAINS"
            self.terminus = "NO TRAINS"
            self.terminus_id = "NO TRAINS"
            self.station = convertSubway(station)
            self.station_id = station
            self.direction = direction
            self.time = "NO TRAINS"
            descriptions = "NO TRAINS"
            self.service_pattern = "NO TRAINS"
            self.service_description = "NO TRAINS"
            self.trip_id = "NO TRAINS"
        else:
            self.route_id = output[1]
            self.terminus = convertSubway(output[2][:-1])
            self.terminus_id = output[2]
            self.station = convertSubway(output[3][:-1])
            self.station_id = output[3]
            self.direction = output[2][-1]
            self.time = output[0]
            descriptions = _routes(output[1])
            self.service_pattern = descriptions[0]
            self.service_description = descriptions[1]
            self.trip_id = output[6]

class gtfsBus(gtfs):
    def __init__(self):
        self.route_id = ""
        self.terminus = ""
        self.terminus_id = ""
        self.stop = ""
        self.stop_id = ""
        self.time = ""
        self.service_pattern = ""
        self.direction = 0
        self.trip_id = ""

    def get(self, stop, direction, responses):
        _validkeyBus(_getAPIBus())
        output = _transitBus(stop, direction, responses, _getAPIBus())
        if (output == "NO BUSES"):
            self.route_id = "NO BUSES"
            self.terminus = "NO BUSES"
            self.terminus_id = "NO BUSES"
            self.stop = stop
            self.stop_id = convertBus(stop)
            self.time = "NO BUSES"
            self.service_pattern = "NO BUSES"
            self.direction = direction
            self.trip_id = "NO BUSES"
        else:
            self.route_id = output[1]
            self.terminus = output[5]
            self.terminus_id = output[2]
            self.stop = output[4]
            self.stop_id = output[3]
            self.time = output[0]
            self.service_pattern = output[7]
            self.direction = output[6]
            self.trip_id = output[8]

    def set(self, route_id, terminus_id, stop_id, time, service_pattern, direction, trip_id):
        self.route_id = route_id
        self.terminus = convertBus(terminus_id)
        self.terminus_id = terminus_id
        self.stop = convertBus(stop_id)
        self.stop_id = stop_id
        self.time = time
        self.service_pattern = service_pattern
        self.direction = direction
        self.trip_id = trip_id

class gtfsLIRR(gtfs):
    def __init__(self):
        self.route_id = ""
        self.terminus = ""
        self.terminus_id = ""
        self.station = "" 
        self.station_id = ""
        self.direction = ""
        self.time = 0
        self.service_pattern = ""
        self.service_description = ""
        self.station_id_list = ""
        self.station_name_list = ""
        self.trip_id = ""

    def get(self, stop, direction, responses):
        _validkeySubway(_getAPILIRR())
        output = _transitLIRR(stop, direction, responses, _getAPILIRR())
        if (output == "NO TRAINS"):
            self.route_id = "NO TRAINS"
            self.terminus = "NO TRAINS"
            self.terminus_id = "NO TRAINS"
            self.station = convertLIRR(stop)
            self.station_id = stop
            self.time = "NO TRAINS"
            self.service_description = "NO TRAINS"
            self.service_pattern = "NO TRAINS"
            self.station_id_list = "NO TRAINS"
            self.station_name_list = "NO TRAINS"
            self.direction = direction
            self.trip_id = "NO TRAINS"
        else:
            self.route_id = output[1]
            self.terminus = convertLIRR(output[2])
            self.terminus_id = output[2]
            self.station = convertLIRR(output[3])
            self.station_id = output[3]
            self.time = output[0]
            self.service_description = f"{timeconvert(output[0])} train to " + convertLIRR(output[2])
            self.service_pattern = convertLIRR(output[2])
            self.station_id_list = output[6]
            self.station_name_list = output[7]
            self.direction = output[4]
            self.trip_id = output[5]

    def set(self, route_id, terminus_id, station_id, direction, time, pattern, description, trip_id, station_id_list):
        self.route_id = route_id
        self.terminus = convertLIRR(terminus_id)
        self.terminus_id = terminus_id
        self.station = convertLIRR(station_id)
        self.station_id = station_id
        self.direction = direction
        self.time = time
        self.service_pattern = pattern
        self.service_description = description
        self.station_id_list = station_id_list
        self.station_name_list = [convertLIRR(i) for i in station_id_list]
        self.trip_id = trip_id

class gtfsMNR(gtfs):
    def __init__(self):
        self.route_id = ""
        self.terminus = ""
        self.terminus_id = ""
        self.station = "" 
        self.station_id = ""
        self.direction = ""
        self.time = 0
        self.service_pattern = ""
        self.service_description = ""
        self.station_id_list = ""
        self.station_name_list = ""
        self.trip_id = ""

    def get(self, stop, direction, responses):
        _validkeySubway(_getAPIMNR())
        output = _transitMNR(stop, direction, responses, _getAPIMNR())
        if (output == "NO TRAINS"):
            self.route_id = "NO TRAINS"
            self.terminus = "NO TRAINS"
            self.terminus_id = "NO TRAINS"
            self.station = convertMNR(stop)
            self.station_id = stop
            self.time = "NO TRAINS"
            self.service_description = "NO TRAINS"
            self.service_pattern = "NO TRAINS"
            self.station_id_list = "NO TRAINS"
            self.station_name_list = "NO TRAINS"
            self.direction = direction
            self.trip_id = "NO TRAINS"
        else:
            self.route_id = output[1]
            self.terminus = convertMNR(output[2])
            self.terminus_id = output[2]
            self.station = convertMNR(output[3])
            self.station_id = output[3]
            self.time = output[0]
            self.service_description = f"{timeconvert(output[0])} train to " + convertMNR(output[2])
            self.service_pattern = convertMNR(output[2])
            self.station_id_list = output[6]
            self.station_name_list = output[7]
            self.direction = output[4]
            self.trip_id = output[5]

    def set(self, route_id, terminus_id, station_id, direction, time, pattern, description, trip_id, station_id_list):
        self.route_id = route_id
        self.terminus = convertMNR(terminus_id)
        self.terminus_id = terminus_id
        self.station = convertMNR(station_id)
        self.station_id = station_id
        self.direction = direction
        self.time = time
        self.service_pattern = pattern
        self.service_description = description
        self.station_id_list = station_id_list
        self.station_name_list = [convertMNR(i) for i in station_id_list]
        self.trip_id = trip_id

def keySubway(string):
    global APISubway
    APISubway = string 

def keyBus(string):
    global APIBus
    APIBus = string 

def keyLIRR(string):
    global APILIRR
    APILIRR = string 

def keyMNR(string):
    global APIMNR
    APIMNR = string 

def _getAPISubway():
    return APISubway

def _getAPIBus():
    return APIBus 

def _getAPILIRR():
    return APILIRR

def _getAPIMNR():
    return APIMNR

def timeconvert(input):
    out = datetime.datetime.now() + datetime.timedelta(minutes=input) 
    return out.strftime('%H:%M')

def _validkeySubway(key):
    if (str(requests.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs", headers={'x-api-key' : key}))) != "<Response [200]>":
        raise Exception("INVALID KEY")

def _validkeyBus(key):
    if (str(requests.get(f'http://bustime.mta.info/api/where/stop/MTA_550320.xml?key={key}'))) != "<Response [200]>":
        raise Exception("INVALID KEY")

def convertBus(input):
    if type(input) != type("") and type(input) != type(0):
        raise Exception("INVALID CLASS: This method requires a String or an Integer")
    if (type(input) == type(0)):
        input = str(input)
    responsestop = requests.get(f'http://bustime.mta.info/api/where/stop/MTA_{input}.xml?key={_getAPIBus()}')
    filenamevar = f"logs/Bustime/{(datetime.datetime.now()).strftime('%d%m%Y')}.xml"
    with open(filenamevar,"wb") as f:
        f.write(responsestop.content)
    tree = ET.parse(filenamevar)
    root = tree.getroot()
    stop_name = root[4][4].text
    return stop_name

def convertSubway(input):
    if type(input) != type(""):
        raise Exception("INVALID CLASS: This method requires a String")
    output = []
    with open('stops.txt','r') as csv_file:
        if (len(input) == 3):
            csv_file = csv.reader(csv_file)
            for row in csv_file:
                if row[2] == input:
                    output.append(row[5])
        else:
   
            raise Exception("INVALID ARGUMENT")
    if (len(output) == 1):
        for i in output: return i
    else:
        return output

def convertLIRR(input):
    output = ""
    if type(input) != type(""):
        raise Exception("INVALID CLASS: This method requires a String")
    if (type(input) == type(0)):
        input = str(input)
    #print(input)
    f = open("lirr_gtfs.json")
    data = json.load(f)
    #print(data["gtfs"]["stops"])
    for i in data["gtfs"]["stops"]:
        if input == i["stop_id"]:
            output = i["stop_name"]
    #print(output)
    return output 

def convertMNR(input):
    output = ""
    if type(input) != type(""):
        raise Exception("INVALID CLASS: This method requires a String")
    if (type(input) == type(0)):
        input = str(input)
    #print(input)
    with open('stations.txt','r') as csv_file:
        csv_file = csv.reader(csv_file)
        for row in csv_file:
            if row[0] == input:
               output = row[2]
    #print(output)
    return output 

def _url():
    link = []
    with open(f"logs/NYCT_GTFS/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","w") as test:
        test.write("")
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-si')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs')
    return link

def _transitSubway(stop, direction, responses, API):
    times = []
    tripids = []
    current_time = datetime.datetime.now()
    links = _url()
    for link in links:
        destination = []
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(link, headers={'x-api-key' : API})
        feed.ParseFromString(response.content)
      
        with open(f"logs/NYCT_GTFS/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","a") as test:
            test.write(str(feed))
        for entity in feed.entity:
            if entity.trip_update:
                for update in entity.trip_update.stop_time_update:
                    if update.stop_id == (stop+direction):
                        time = update.arrival.time
                        if time <= 0:
                                time = update.departure.time
                        time = datetime.datetime.fromtimestamp(time)
                        time = math.trunc(((time - current_time).total_seconds()) / 60)
                        for update in entity.trip_update.stop_time_update:
                                destination.append(update.stop_id)
                        tripids.append(entity.trip_update.trip.trip_id)
                
                        times.append([time, entity.trip_update.trip.route_id, destination[-1], stop+direction])
     
    times.sort()
    fallback = times.copy()
    temp = 0
    while (temp <= (len(times) - 1)):
        if (times[temp][0] < 1):
            times.pop(temp)
            temp = -1
        else:
            with open('stops.txt','r') as csv_file:
                csv_file = csv.reader(csv_file)
                for row in csv_file:
                    if row[2] == fallback[temp][2][:-1]:
                        times[temp].append(f'{row[5]}')
            with open('stops.txt','r') as csv_file:
                csv_file = csv.reader(csv_file)
                for row in csv_file:
                    if row[2] == fallback[temp][3][:-1]:
                        times[temp].append(f'{row[5]}')

        if (times[temp][1] == "5X"):
            times[temp][1] = "5"
        elif (times[temp][1] == "H"):
            times[temp][1] = "SR"
        elif (times[temp][1] == "FS"):
            times[temp][1] = "SF"
        elif (times[temp][1] == "GS"):
            times[temp][1] = "S"
        else:
            times[temp][1] = times[temp][1].upper()
        temp += 1
    
    try:
        times = [times[responses-1]]
    except:
        return "NO TRAINS"

    output = []
    for item in times:
        output.append(item)
    output.append(tripids[responses-1])
   
    with open(f"logs/Print/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","a") as test:
        test.write(str(output)+ f" {datetime.datetime.now()}\n")
    return output

def _transitBus(stop, direction, responses, API):
    current_time = datetime.datetime.now()
    times = []
    destination = []
    response = requests.get(f"http://gtfsrt.prod.obanyc.com/tripUpdates?key={API}")
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    with open(f"logs/Bustime/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","w") as test:
        test.write(str(feed)+ f" {datetime.datetime.now()}\n")
 
    for entity in feed.entity:
        for update in entity.trip_update.stop_time_update:
       
            if ((update.stop_id == stop) and (str(entity.trip_update.trip.direction_id) == str(direction))):
         
                time = update.arrival.time
                if (time < 0):
                    time = update.departure.time
                time = datetime.datetime.fromtimestamp(time)
                time = math.trunc(((time - current_time).total_seconds()) / 60)
                if (time < 0):
                    continue 
                trip_id = entity.trip_update.trip.trip_id
                route_id = entity.trip_update.trip.route_id
                for update in entity.trip_update.stop_time_update:
                    destination.append(update.stop_id)
                terminus_id = destination[-1]
                direction = entity.trip_update.trip.direction_id
                stop_id = update.stop_id
           
                responsestop = requests.get(f'http://bustime.mta.info/api/where/stop/MTA_{stop}.xml?key={API}')
                filenamevar = f"logs/Bustime/{(datetime.datetime.now()).strftime('%d%m%Y')}.xml"
         
                with open(filenamevar,"wb") as f:
                    f.write(responsestop.content)
                tree = ET.parse(filenamevar)
                root = tree.getroot()
                stop_name = root[4][4].text
                for item in root[4][7]:
                    if (item[1].text == route_id):
                        service_pattern = item[3].text
                responsestop = requests.get(f'http://bustime.mta.info/api/where/stop/MTA_{terminus_id}.xml?key={API}')
                filenamevar = f"logs/Bustime/{(datetime.datetime.now()).strftime('%d%m%Y')}.xml"
               
                with open(filenamevar,"wb") as f:
                    f.write(responsestop.content)
                tree = ET.parse(filenamevar)
                root = tree.getroot()
                terminus_name = root[4][4].text
               
                times.append([time, route_id, terminus_id, stop_id, stop_name, terminus_name, direction, service_pattern, trip_id])
                
    times.sort()
    try:
        times = times[responses-1]
    except:
        return "NO BUSES"

    with open(f"logs/Print/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","a") as test:
        test.write(str(times)+ f" {datetime.datetime.now()}\n")
    return times 

def  _transitLIRR(stop, direction, responses, API):
    current_time = datetime.datetime.now()
    times = []
    destination = []
    #print(API)
    response = requests.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/lirr%2Fgtfs-lirr", headers={'x-api-key' : API})
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    with open(f"logs/LIRR/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","w") as test:
        test.write(str(feed)+ f" {datetime.datetime.now()}\n")
    for entity in feed.entity:
        for update in entity.trip_update.stop_time_update:
            if ((update.stop_id == stop) and (str(entity.trip_update.trip.direction_id) == str(direction))):
                station_id = update.stop_id
                time = update.arrival.time
                if (time < 0):
                    time = update.departure.time
                time = datetime.datetime.fromtimestamp(time)
                time = math.trunc(((time - current_time).total_seconds()) / 60)
                #print(time)
                if (time < 0):
                    continue 
                trip_id = entity.trip_update.trip.trip_id
                route_id = entity.trip_update.trip.route_id
                direction = entity.trip_update.trip.direction_id
                station_id_list = []
                for update in entity.trip_update.stop_time_update:
                    destination.append(update.stop_id)
                    station_id_list.append(update.stop_id)
                #print(service_description)
                station_stop_list = [convertLIRR(i) for i in station_id_list]
                terminus_id = destination[-1]
            
                #print(stop)

                times.append([time, route_id, terminus_id, station_id, direction, trip_id, station_id_list, station_stop_list])
                #print(data["gtfs"]["stops"])
                #for i in data["gtfs"]["stops"]:
                #print(i["stop_id"] + " " + i["stop_name"])
    times.sort()
    #times = []
    #print(times)
    try:
        times = times[responses-1]
    except:
        return "NO TRAINS"
        #print(times)

    with open(f"logs/Print/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","a") as test:
        test.write(str(times)+ f" {datetime.datetime.now()}\n")
    return times 

def  _transitMNR(stop, direction, responses, API):
    current_time = datetime.datetime.now()
    times = []
    destination = []
    #print(API)
    response = requests.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/mnr%2Fgtfs-mnr", headers={'x-api-key' : API})
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    with open(f"logs/MNR/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","w") as test:
        test.write(str(feed)+ f" {datetime.datetime.now()}\n")
    for entity in feed.entity:
        for update in entity.trip_update.stop_time_update:
            if ((update.stop_id == stop) and (str(entity.trip_update.trip.direction_id) == str(direction))):
                station_id = update.stop_id
                time = update.arrival.time
                if (time < 0):
                    time = update.departure.time
                time = datetime.datetime.fromtimestamp(time)
                time = math.trunc(((time - current_time).total_seconds()) / 60)
                #print(time)
                if (time < 0):
                    continue 
                trip_id = entity.trip_update.trip.trip_id
                route_id = entity.trip_update.trip.route_id
                direction = entity.trip_update.trip.direction_id
                station_id_list = []
                for update in entity.trip_update.stop_time_update:
                    destination.append(update.stop_id)
                    station_id_list.append(update.stop_id)
                #print(service_description)
                station_stop_list = [convertMNR(i) for i in station_id_list]
                terminus_id = destination[-1]
            
                #print(stop)

                times.append([time, route_id, terminus_id, station_id, direction, trip_id, station_id_list, station_stop_list])
                #print(data["gtfs"]["stops"])
                #for i in data["gtfs"]["stops"]:
                #print(i["stop_id"] + " " + i["stop_name"])
    times.sort()
    #times = []
    #print(times)
    try:
        times = times[responses-1]
    except:
        return "NO TRAINS"
        #print(times)

    with open(f"logs/Print/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","a") as test:
        test.write(str(times)+ f" {datetime.datetime.now()}\n")
    return times 
    

def _routes(service):
    with open('routes.txt','r') as csv_file:
        csv_file = csv.reader(csv_file)
        for row in csv_file:
            if row[0] == service:
                return row[3], row[4], row[6]

def main():
    keyLIRR("p4G33OQzU8acTdI6FbwCQ3C4bXKbmLFla5ZSDvdc")
    keySubway("p4G33OQzU8acTdI6FbwCQ3C4bXKbmLFla5ZSDvdc")
    keyMNR("p4G33OQzU8acTdI6FbwCQ3C4bXKbmLFla5ZSDvdc")
    
    #response = requests.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/mnr%2Fgtfs-mnr", headers={'x-api-key' : _getAPIMNR()})
    #feed = gtfs_realtime_pb2.FeedMessage()
    #feed.ParseFromString(response.content)
    #with open(f"logs/MNR/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","w") as test:
    #    test.write(str(feed)+ f" {datetime.datetime.now()}\n")


main()
