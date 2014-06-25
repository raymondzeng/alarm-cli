#!/usr/local/bin/python

import itunes
import sys

def main(args):
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
