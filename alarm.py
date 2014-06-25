import time
from datetime import datetime, timedelta
import sys
import os
from subprocess import check_output, CalledProcessError
import itunes

this_dir, _ = os.path.split(__file__)

import string

# path to the plist to load into launchd
# a new one is created for every new alarm with create_plist
# so there can only be one alarm at a time
PLIST = os.path.join(this_dir, 'itunes_alarm.plist')

def set_alarm(hour, minute,
              info='whatever your iTunes is currently playing',
              query=None, index=None):

    # basically a dictionary
    # [year, month, day, hour, minute, second, weekday, _, _]
    time_now = datetime.now()

    # for now, the date is always _today_
    alert_time = datetime(time_now.year, time_now.month, time_now.day, 
                          hour, minute)

    diff = alert_time - time_now
    
    if time_now > alert_time:
        print "Can't set alarm in the past.\nCurrent time: " + time_now.strftime('%H:%M:%S')
        return

    dt_string = alert_time.strftime('%m/%d/%y %H:%M:%S')
    
    # calc hours, mins, and secs in the difference of time now and alarm
    hours, remainder = divmod(diff.seconds, 3600)
    mins, secs = divmod(remainder, 60)

    from_now = '%d hours, %d minutes, %d seconds' % (hours, mins, secs)

    # hacky work around
    # if query is None, it will be passed to the script run by launchd 
    # as the string 'None', and since that may be a valid query
    new_query = query
    new_index = index
    if new_query is None:
        new_query = '@@@none@@@'
        new_index = '@@@none@@@'

    create_plist(time_now.year, time_now.month, time_now.day,
                 hour, minute, new_query, new_index)

     # wake up machine before alarm plays to allow ample time 
     # for launchd to get ready
    wake_time = alert_time - timedelta(0, -30)
    wake_string = wake_time.strftime('%m/%d/%y %H:%M:%S')

    try:
        print PLIST
        check_output(['pmset', 'schedule', 'wakeorpoweron', wake_string])
        # unloads any old one
        check_output(['launchctl', 'unload', PLIST])
        # loads the new one we created with create_plist
        check_output(['launchctl', 'load', PLIST])
        #check_output(['python', 'play_itunes.py', new_query, new_index])
    except CalledProcessError, e:
        print e.output + ' Please try again'
        return

    s = '{head}Alarm scheduled for {dt}\n{head}in {fn}\n{head}with {song}' 
    d = {'head' : '[alarm]\t',
         'dt'   : dt_string, 
         'fn'   : from_now,
         'song' : info}
    
    print s.format(**d)


# not sure if launchd uses year and second so keeping the params
# though not using them
def create_plist(year, month, day, hour, minute,
                 query, index):
    template_file = open(os.path.join(this_dir, 'template.txt'), 'rb')
    src = string.Template(template_file.read())
    template_file.close()

    d = {'label' : 'com.ray.alarm',
        # 'script_path' : '/usr/local/lib/python2.7/site-packages/alarm-0.1-py2.7.egg/alarm/play_itunes.py',
         'script_path' : os.path.abspath('play_itunes.py'),
         'month' : month,
         'day' : day,
         'hour' : hour,
         'minute' : minute,
         'query' : query,
         'index' : index}

    new_src = src.substitute(d)
    
    new_file = open(os.path.join(this_dir, 'itunes_alarm.plist'), 'w')
    new_file.write(new_src)
    new_file.close()

def main():
    if os.getuid() != 0:
        print 'You must run this as root. Exiting.'
    else:
        args = sys.argv
        
        if len(args) == 3:
            ints = [int(x) for x in args[1:]]
            set_alarm(ints[0], ints[1])
        elif len(args) > 4 and args[3] == '-i':
            ints = [int(x) for x in args[1:3]]

            if len(args) == 6:
                index = args[5] 
                if index.isdigit():
                    index = int(index)
                else:
                    print 'Index must be an integer'
                    pass
            else:
                index = None

            query = args[4]
            info = itunes.searchPlay(query, index=index)
            if info != None:
                set_alarm(ints[0], ints[1],
                          info=info, query=query, index=index)
            else:
                pass
        else:
            print 'Usage: sudo alarm <hour> <minute> [-i <song> [<index>]]\HT\nhour is in 24hr format\n-i optional flag followed by a query to select a song from your itunes library\nIf there is exactly one result from your query, it will be used.\nIf there is more than one, all results will be displayed and you must add an index number at the end of your query indicating which song you chose.\n\nExample: sudo alarm 17 30 -i Rain 2'
            

if __name__ == '__main__':
    main()
