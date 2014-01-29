import time

alarmtime = 0

def handleAlarm(cal, sound):
    if alarmtime != 0 and alarmtime < time.time():
        diff = time.time() - alarmtime
        #start alarm sound
        if diff > 5:
            cal.set("BedLamp",1)
        elif diff > 20:
            cal.set("RoofLamp",1)

        if cal.get("AlarmSwitch") == 1:
            cal.set("WaterBoiler",1)
            cal.set("BedMassage",1)
            #stop alarm sound
        