import datetime

def currenttime():
    now = (datetime.datetime.now()).strftime("%m %d, %Y %H:%M")
    return now 

print(currenttime()) 

