# Taken and modified from this very cool library:
#     author="Anshu Chimala",
#     author_email="me@achimala.com",
#     license="GPLv3",
#     url="https://github.com/achimala/itunes-cli",

import sys
import argparse
from appscript import app, k

# Reference to the iTunes application
iTunes = app('iTunes')

def stop():
    iTunes.pause()

# searches if play is false
# plays if play is true and possible
def searchPlay(query=False, index=None, play=False):    

    def info(result):
        return '"{}" | "{}" | "{}"'.format(
            result.name.get().encode('utf-8'),
            result.artist.get().encode('utf-8'), 
            result.album.get().encode('utf-8'))

    if not query and play:
        iTunes.play()
        return

    where = k.all       
    playlist = iTunes.playlists['Library']
    results = iTunes.search(playlist, for_=query, only=where)
    
    if len(results) == 0:
        print "No results"
        return None
        
    if len(results) == 1:
        if play:
            results[0].play()
            return
        else:
            return info(results[0])
    
    if len(results) >= 1:
        if index is not None:
            if type(index) == int and index < len(results):
                if play:
                    results[index].play()
                    return
                else:
                    return info(results[index])
            else:
                print "Invalid index:", index
            return None
            
        table = []
        longest = [0, 0, 0]
        artist_set = set()
        album_set = set()
        
        MAXLEN = 40
        for (i, song) in enumerate(results):
            name, artist, album = song.name.get(), song.artist.get(), song.album.get()
            longest[0] = min(MAXLEN, max(longest[0], len(name)))
            longest[1] = min(MAXLEN, max(longest[1], len(artist)))
            longest[2] = min(MAXLEN, max(longest[2], len(album)))
            artist_set.add(artist)
            album_set.add(album)
            table.append((i, name, artist, album))
            
        fmt = ('{{:<7}} | {{:<{}}} | {{:<{}}}').format(*longest)
        print "Add an index at the end of your command to select a song"
        print fmt.format('index', 'name', 'artist') 
        print fmt.format(*map(lambda x: '-'*x, [7]+longest))

        for (i, song) in enumerate(results):
            name = song.name.get()
            artist = song.artist.get()
            album = song.album.get()
            
            if len(name)   > longest[0]: 
                name   = name[:longest[0]-3]   + '...'
            if len(artist) > longest[1]: 
                artist = artist[:longest[1]-3] + '...'   
                 
            print fmt.format(i, name.encode('utf-8'), 
                             artist.encode('utf-8'))
                
