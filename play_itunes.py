#!/usr/local/bin/python

import itunes
import sys
from subprocess import check_output, CalledProcessError

def main(args):
    wakeup_string = args[3]
    
    # cancel the wakeup in case there still is
    try:
        check_output(['pmset', 'schedule', 'cancel', 
                      'wakeorpoweron', wakeup_string, 'alarm-cli'])
    except CalledProcessError, e:
        print e.output
    
    # assumes args are exactly as they should be and are valid
    # TODO: args parsing error    
    query = args[1]
    index = args[2] 
    
    if query == '@@@none@@@':
        query = None

    if index == '@@@none@@@':
        index = None
    else:
        index = int(index)

    itunes.searchPlay(query=query, index=index, play=True)
    
if __name__ == "__main__":
    # always
    # play_itunes.py query index
    main(sys.argv)
