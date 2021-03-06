Commandline Alarm Clock
===
A command line alarm clock utility that uses music from your iTunes library. Works even if your computer is asleep, just like an alarm clock worth its name would.

Warning: If laptop lid is down and setting is to put computer to sleep if lid down, song will play for about 5 seconds and then stop.

Only works with OSX because AppleScript is required to talk to iTunes and `launchd` is required for setting up tasks.

How to use
===

Clone the repo or download just these files:
```
alarm.py
play_itunes.py
itunes.py
template.txt
```
You need to run as root.

Run with `python alarm.py <hour> <minute> [-i <query> [<index>]]`

Without any optional params, so just `python alarm.py <hour> <minute>` will set an alarm for today at hour:minute and whatever song is currently queued in your iTunes will be played.

Using the `-i` flag, you can search and select songs from your iTunes library. The query is the same as enetering it directly into the iTunes search bar. Multi-word queries must be enclosed with quotation marks. 

If your query has no results, it will give you a no-results-message and not set an alarm.

If there is exactly one result for your query, you don't need to specify an index and that one result will be chosen. For example, `python alarm.py <hour> <minute> -i "very specific query that only has one match"`. 

If there is more than one result, you will be shown an indexed table of the results. You will need to add an index to your command. For example,

```
compooter$ sudo python alarm.py 10 10 -i rain
Add an index at the end of your command to select a song
index   | name                        | artist        
------- | --------------------------- | --------------
0       | Set Fire To The Rain        | Adele         
1       | Hey, Soul Sister            | Train         
2       | Kiss The Rain               | Yiruma        
3       | Sad Tango                   | 비 (Rain)    
compooter$ 
compooter$ sudo python alarm.py 10 10 -i rain 2
```
When the alarm "rings", to "shut it off", just pause or stop iTunes the same way you normally would.

How it works
===
1. If `-i` flag used, searches iTunes and if that process results with one song, moves on to step 2, otherwise prints stuff and quits. If `-i` flag not used, skips to step 2.
2. Checks that you aren't setting an alarm in the past
3. Creates a `.plist` config file to be executed by `launchd`
4. The `.plist` stores the time to execute as well as the query and index which result in one song
5. Makes a call to `pmset` to schedule a wakeup at the chosen time
6. Make calls to `launchctl` to load the `.plist` file we created
7. `alarm.py` exits  

8. `pmset` is set to wake up the computer a set number of seconds before the alarm time
9. At alarm time, `launchd` executes the `.plist` file which will call `play_itunes.py`, passing to it the query and index it stored
10. `play_itunes.py` searches with the query and index the same way as in step 1, but this time with a `play=True` flag so after it searches, it will also tell iTunes to start playing.



Testing
===

### Battery Power
> Settings:
> Computer Sleep	: 8 minutes
> Display Sleep 	: 5 minutes
> Put hard drives sleep : True
> Enable Power Nap 	: False

Trials: 
10 minutes (Menu Sleep)
20 minutes (Lid closed) [warning: only plays for 5s before goes back to sleep]
6 hours 20 minutes (Corner Display Sleep)

### Adapter Power
> Settings:
> Computer Sleep	: 20 minutes
> Display Sleep 	: 11 minutes
> Put hard drives sleep : True
> Enable Power Nap 	: True

