A command line alarm clock utility that uses music from your iTunes library. 

Only works with OSX because AppleScript is required to talk to iTunes. 

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
rayz:alarm-cli raymondzeng$ sudo python alarm.py 10 10 -i rain
Add an index at the end of your command to select a song
index   | name                        | artist        
------- | --------------------------- | --------------
0       | Set Fire To The Rain        | Adele         
1       | Innocent                    | Our Lady Peace
2       | Hey, Soul Sister            | Train         
3       | Kiss The Rain               | Yiruma        
4       | Sad Tango                   | 비 (Rain)    
5       | Love Story (0912....그 이후) | 비 (Rain)    
6       | But I Love You              | 비 (Rain)    
7       | In My Bed                   | 비 (Rain)    
8       | Move On                     | 비 (Rain)    
rayz:alarm-cli raymondzeng$ 
rayz:alarm-cli raymondzeng$ sudo python alarm.py 10 10 -i rain 2
```

Tested:

### Battery Power
> Settings:
> Computer Sleep	: 8 minutes
> Display Sleep 	: 5 minutes
> Put hard drives sleep : True
> Enable Power Nap 	: False

Trials: 
10 minutes (Menu Sleep)

### Adapter Power
> Settings:
> Computer Sleep	: 20 minutes
> Display Sleep 	: 11 minutes
> Put hard drives sleep : True
> Enable Power Nap 	: True

