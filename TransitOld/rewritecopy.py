import requests, csv, datetime, math, time
import gtfs_realtime_pb2, nyct_subway_pb2

API = 'p4G33OQzU8acTdI6FbwCQ3C4bXKbmLFla5ZSDvdc'

def url():
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


def transit(stop, direction):
    times = []
    current_time = datetime.datetime.now()
    links = url()
    for link in links:
        destination = []
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(link, headers={'x-api-key' : API})
        feed.ParseFromString(response.content)
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
                        times.append([time,entity.trip_update.trip.route_id, destination[-1][:-1]])
    times.sort()
    for time in times:
            if time[0] < 0:
                    times.remove(time)
            with open('stops.txt','r') as csv_file:
                    csv_file = csv.reader(csv_file)
                    for row in csv_file:
                            if row[2] == time[2]:
                                    time.append(f'{row[5]} ({row[2]})')
                                    time.pop(2)
            with open('stops.txt','r') as csv_file:
                csv_file = csv.reader(csv_file)
                for row in csv_file:
                        if row[2] == stop:
                                name = row[5]
    times = times[:3]
    output = []
    output.append(name)
    output.append(times)
    return output 



