import requests, csv, datetime, math, time
import xml.dom.minidom
import xml.etree.ElementTree as ET
import gtfs_realtime_pb2, nyct_subway_pb2

API = ""

class gtfsSubway:
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
        self.schedule = ""

    def set(self, route_id, terminus_id, station_id, direction, time, pattern, description, link):
        self.route_id = route_id
        self.terminus = convertSubway(terminus_id)
        self.terminus_id = terminus_id
        self.station = convertSubway(station_id)
        self.station_id = station_id
        self.direction = direction
        self.time = time
        self.service_pattern = pattern
        self.service_description = description
        self.schedule = link

    def get(self, station, direction, responses):
        _validkey(_getAPI())
        output = _transit(station, direction, responses, _getAPI())
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
        self.schedule = descriptions[2]

class gtfsBus:
    def __init__(self):
        self.route_id = ""
        self.terminus = ""
        self.terminus_id = ""
        self.stop = ""
        self.stop_id = ""
        self.time = ""
        self.service_pattern = ""

def key(string):
    global API
    API = string 

def _getAPI():
    return API

def _validkey(key):
    if (str(requests.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs", headers={'x-api-key' : key}))) != "<Response [200]>":
        raise Exception("INVALID KEY")

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
            '''
            csv_file = csv.reader(csv_file)
            for row in csv_file:
                if row[5] == input:
                    output.append(row[2])
            '''
            raise Exception("INVALID ARGUMENT")
    if (len(output) == 1):
        for i in output: return i
    else:
        return output

def _url():
    link = []
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-si')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l')
    link.append('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs')
    return link

def _transit(stop, direction, responses, API):
    times = []
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
    
    times = times[responses-1]
    output = []
    for item in times:
        output.append(item)
    with open(f"logs/Print/{(datetime.datetime.now()).strftime('%d%m%Y')}.txt","a") as test:
        test.write(str(output)+ f" {datetime.datetime.now()}\n")
    return output

def _routes(service):
    with open('routes.txt','r') as csv_file:
        csv_file = csv.reader(csv_file)
        for row in csv_file:
            if row[0] == service:
                return row[3], row[4], row[6]

def bustime():
    thing = "6f064d4d-ed7d-415a-9d4a-c01204897506"
    response = requests.get(f"http://gtfsrt.prod.obanyc.com/tripUpdates?key={thing}")
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    #print(feed.entity)
    for entity in feed.entity:
        if (entity.trip_update.trip.route_id == "S78"):
            #print(entity.trip_update)
            pass
    responsestop = requests.get(f'http://bustime.mta.info/api/where/stop/MTA_550320.xml?key={thing}')
    filenamevar = f"logs/Bustime/{(datetime.datetime.now()).strftime('%d%m%Y')}.xml"
    with open(filenamevar,"wb") as test:
        test.write(responsestop.content)
    #doc = xml.dom.minidom.parse(filenamevar)
    #print(doc.firstChild.tagName)
    tree = ET.parse(filenamevar)
    root = tree.getroot()
    print(root[4][4].text)
    return 0

#bustime()
