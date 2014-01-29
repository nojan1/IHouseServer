import time

class LimitedList(list):
    def __init__(self):
        list.__init__(self)

    def append(self,item):
        list.append(item)
        if list.count == 50:
            list.pop(0)

alarmActive = False
isBuzzing = False
isLarming = False
motions = LimitedList()
dooropenings = LimitedList()
lastTimeRun = 0


def alarmState(list):
    if alarmActive == False:
        return False

    #check if there is more than 10 ocurenses within 2 secs
    return False
        
def handleSecurity(cal,soundhandler):
    SECS = time.time()
    global lastTimeRun, alarmActive, isBuzzing, isLarming, motions, dooropenings
    if SECS - lastTimeRun > 0.2:
        lastTimeRun = SECS
        if cal.get("MainDoor") == 1:
            dooropenings.append(SECS)

        if cal.get("LowerMotion") == 1:
            motions.append(SECS)

        if alarmState(motions) or alarmState(dooropenings):
            if isBuzzing == False:
                isBuzzing = SECS
                #buzzzzzzzz
            elif SECS - isBuzzing > 10:
                if isLarming == False:
                    isLarming = SECS
                    #sound alarm looping
        else:
            if isLarming != False:
                #stop alarm
                pass
            if isBuzzing != False:
                #stop buzzer
                pass
                
            isBuzzing = False
            isLarming = False


