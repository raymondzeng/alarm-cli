import time
from datetime import datetime
from appscript import app
import sys
import os
from subprocess import call
import itunes

iTunes = app("iTunes")

def set_alarm(hour, minute, sec):
    # basically an array
    # [year, month, day, hour, minute, second, weekday, _, _]
    time_now = datetime.now()

    # for now, the date is always _today_
    alert_time = datetime(time_now.year, time_now.month, time_now.day, 
                          hour, minute, sec)

    diff = alert_time - time_now
    diff_in_sec = diff.days * 86400 + diff.seconds
   
    if diff_in_sec <= 0:
        print "Can't set alarm in the past.\nCurrent time: " + time_now.strftime("%H:%M:%S")
        return

    dt_string = alert_time.strftime("%m/%d/20%y %H:%M:%S")

    call(["pmset", 'schedule', 'wakeorpoweron', dt_string])
    print "[alarm]\tAlarmed scheduled for " + dt_string

    time.sleep(diff_in_sec)
    iTunes.play()
    stop = raw_input("[alarm]\tPress any key to shutoff alarm:\n")
    iTunes.stop()

if __name__ == "__main__":
    if os.getuid() != 0:
        print "You must run this as root. Exiting."
    else:
        args = sys.argv
        
        if len(args) == 4:
            ints = [int(x) for x in args[1:]]
            set_alarm(ints[0], ints[1], ints[2])
        elif len(args) > 5 and args[4] == '-i':
            ints = [int(x) for x in args[1:4]]
            # set_alarm(ints[0], ints[1], ints[2])
            itunes.play(args[5], index=None, songs=False, 
                        albums=False, library=True, artists=False)
        else:
            print "Usage: "
            
