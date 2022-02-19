import stua
stua.keySubway("dsYgCLaGKx5dZFnegn7D59qtcdomLuYS1Y7kScKk")

newtrains = []
x = 0
while True:
    #print(x+1)
    newtrains.append(stua.gtfsSubway())
    newtrains[x].get("137","S",x+1)
    if (newtrains[x].route_id == "NO TRAINS"):
        break 
    print(f'{newtrains[x].time} minutes ({newtrains[x].route_id} to {newtrains[x].terminus} with ID {newtrains[x].trip_id})')
    x += 1

stationName = stua.convertSubway("137")
print(f'Next Southbound trains at {stationName} Subway Station')

for train in newtrains:
    print(f'{train.time} minutes ({train.route_id} to {train.terminus} with ID {train.trip_id})')
