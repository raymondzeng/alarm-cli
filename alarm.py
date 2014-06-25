import time
from datetime import datetime
import sys
from os import getuid
from subprocess import check_output, CalledProcessError
import itunes

def set_alarm(hour, minute, sec, 
              info='whatever your iTunes is currently playing',
              query=None, index=None):

    # basically a dictionary
    # [year, month, day, hour, minute, second, weekday, _, _]
    time_now = datetime.now()

    # for now, the date is always _today_
    alert_time = datetime(time_now.year, time_now.month, time_now.day, 
                          hour, minute, sec)


    diff = alert_time - time_now
    
    if time_now > alert_time:
        print "Can't set alarm in the past.\nCurrent time: " + time_now.strftime("%H:%M:%S")
        return

    dt_string = alert_time.strftime("%m/%d/%y %H:%M:%S")
    
    # calc hours, mins, and secs in the difference of time now and alarm
    hours, remainder = divmod(diff.seconds, 3600)
    mins, secs = divmod(remainder, 60)

    from_now = '%d hours, %d minutes, %d seconds' % (hours, mins, secs)

    try:
        check_output(["pmset", 'schedule', 'wakeorpoweron', dt_string])
    except CalledProcessError, e:
        print e.output + '\nPlease try again'
        return

    s = "{head}Alarm scheduled for {dt}\n{head}in {fn}\n{head}with {song}" 
    d = {'head' : '[alarm]\t',
         'dt'   : dt_string, 
         'fn'   : from_now,
         'song' : info}
    
    print s.format(**d)

    try: 
        time.sleep(diff.seconds)
    except KeyboardInterrupt:
        print "Shutting off alarm"
        return

    itunes.searchPlay(query=query, index=index, play=True)

    inp = raw_input("[alarm]\tPress any key to shutoff alarm:\n")
    if inp == '':
        itunes.stop()
    else:
        return

if __name__ == "__main__":
    if getuid() != 0:
        print "You must run this as root. Exiting."
    else:
        args = sys.argv
        
        if len(args) == 4:
            ints = [int(x) for x in args[1:]]
            set_alarm(ints[0], ints[1], ints[2])
        elif len(args) > 5 and args[4] == '-i':
            ints = [int(x) for x in args[1:4]]

            if len(args) == 7:
                index = args[6] 
                if index.isdigit():
                    index = int(index)
                else:
                    print "Index must be an integer"
                    pass
            else:
                index = None

            query = args[5]
            info = itunes.searchPlay(query, index=index)
            if info != None:
                set_alarm(ints[0], ints[1], ints[2], 
                          info=info, query=query, index=index)
            else:
                pass
        else:
            print "Usage: sudo alarm <hour> <minute> <second> [-i <song> [<index>]]\n\nhour is in 24hr format\n-i optional flag followed by a query to select a song from your itunes library\nIf there is exactly one result from your query, it will be used.\nIf there is more than one, all results will be displayed and you must add an index number at the end of your query indicating which song you chose.\n\nExample: sudo alarm 17 30 0 -i Rain 2"
            
