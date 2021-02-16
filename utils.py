import matplotlib.pyplot as plt
import json
import numpy
import pandas as pd
import datetime


def plotGraph(y, time, action):
    userInput = ("Enter if you want to plot KeyUp or KeyDowns")
    data = y
    x = list(range(len(data)))

    # Average
    average = numpy.mean(data)
    # Words Per Minute = (Chr / 5) / Time
    wpm = 1000 * len(data) / time

    # MatPlotLib Handling
    plt.title("Time Elapsed Between "+action+" Events")
    plt.ylabel("Key Number")
    plt.ylabel("Milliseconds")
    plt.plot(x, y)
    # Format average display box
    plt.text(5, 35, ("WPM: ", wpm, "Average", average) ,style='italic',
        bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
    plt.show()
	

def gettimeBetweenUPS(ksdf):
    action = 'Up'
    ups = list(ksdf[ksdf.action == action].time)
    time = ups[len(ups) - 1] - ups[0]
    time_between_ups = []
    while len(ups) > 1:
         #Get the time from the tuple
        startTime = ups.pop(0)
        betweenTime = ups[0] - startTime
        time_between_ups.append(betweenTime)
        #average = numpy.mean(time_between_downs)
    return (time_between_ups)

def timeBetweenUPS(ksdf):
    action = 'Up'
    ups = list(ksdf[ksdf.action == action].time)
    time = ups[len(ups) - 1] - ups[0]
    plotGraph(gettimeBetweenUPS(ksdf), time, action)
	

def gettimeBetweenDOWNS(ksdf):
    action = 'Down'
    downs = list(ksdf[ksdf.action == action].time)
    time_between_downs = []
    time = downs[len(downs) - 1] - downs[0]
    while len(downs) > 1:
        startTime = downs.pop(0) #Get the time from the tuple
        betweenTime = downs[0] - startTime
        time_between_downs.append(betweenTime)
        #average = numpy.mean(time_between_downs)
    return time_between_downs
    
def timeBetweenDOWNS(ksdf):
    action = 'Down'
    downs = list(ksdf[ksdf.action == action].time)
    time = downs[len(downs) - 1] - downs[0]
    plotGraph(gettimeBetweenDOWNS(ksdf), time, action)
	
	
def gettimeHoldingKey(ksdf):
    action = 'Hold'
    time_holding_key = []
    ups = list(ksdf[ksdf.action == 'Up'].time)
    downs = list(ksdf[ksdf.action == 'Down'].time)
    time = downs[len(downs) - 1] - downs[0]
    while len(downs) > 1:
        downTime = downs.pop(0)
        holdTime = ups.pop(0) - downTime
        time_holding_key.append(holdTime)
        #average = numpy.mean(time_between_downs)
    return time_holding_key
    
def timeHoldingKey(ksdf):
    action = 'Hold'
    downs = list(ksdf[ksdf.action == 'Down'].time)
    time = downs[len(downs) - 1] - downs[0]
    plotGraph(gettimeHoldingKey(ksdf), time, action)
	
	
def gettimeBetweenKey(ksdf):
    action = 'Between'
    time_between_key = []
    ups = list(ksdf[ksdf.action == 'Up'].time)
    downs = list(ksdf[ksdf.action == 'Down'].time)
    del downs[0]
    time = downs[len(downs) - 1] - downs[0]
    while len(ups) > 1:
        upTime = ups.pop(0)
        betweenTime = downs.pop(0) - upTime
        time_between_key.append(betweenTime)
        #average = numpy.mean(time_between_downs)
    return time_between_key
    
def timeBetweenKey(ksdf):
    action = 'Between'
    downs = list(ksdf[ksdf.action == 'Down'].time)
    time = downs[len(downs) - 1] - downs[0]
    plotGraph(gettimeBetweenKey(ksdf), time, action)
	
	
def getUserSnDict(userdf):
    uniqUsers = set(userdf.username)
    userSnDict = {}
    for user in uniqUsers:
        sessions = set()
        if not user in userSnDict:
            userSnDict[user] = list()
        for sn in userdf[userdf.username == user].sn:
            if sn not in sessions:
                userSnDict[user].append(sn)
            sessions.add(sn)
    return userSnDict
	
	
def getX(fdf):
    phrase = 'dslhbyj'
    X = pd.DataFrame()
    usnd = getUserSnDict(fdf[fdf.phrase == phrase])
    for user in usnd:
        for sn in usnd[user]:
            df = fdf[(fdf.sn == sn) & (fdf.username == user)]
            if df.shape[0] != len(phrase)*2:
                continue
            features_df = pd.DataFrame([[user] + [sn] +
            gettimeBetweenDOWNS(df) + 
            gettimeBetweenUPS(df) +
            gettimeBetweenKey(df) +
            gettimeHoldingKey(df)])
            X = pd.concat([X, features_df], ignore_index=True)
    return X
