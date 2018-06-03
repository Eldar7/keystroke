import pyHook
import pythoncom
import json
import os
import pandas as pd
import sys
import datetime


def getUserFileWriteSession():
    print("File Location: ", os.getcwd())
    global username
    username = input("Enter your username: ")
    sys.stdout.flush()


def get_next_sn_by_user(username, df):
    try:
        next_sn = max(df[df.username == username].sn) + 1
    except:
        next_sn = 0
    return next_sn


def addSNtoUser(username, df, dfToAdd, phrase):
    sn = get_next_sn_by_user(username, df)
    date = datetime.datetime.now()
    dftmp = pd.DataFrame([[username, sn, phrase, date]], columns=['username', 'sn', 'phrase', 'date'])

    ndf = pd.DataFrame()
    ndf = ndf.append(dftmp).join(dfToAdd, how='right')

    ndf.username = ndf.username.fillna(username)
    ndf.sn = ndf.sn.fillna(sn)
    ndf.phrase = ndf.phrase.fillna(phrase)
    ndf.date = ndf.date.fillna(date)

    return pd.concat([df, ndf], ignore_index=True)


def userRecordData(eventList):
    userFile = 'userdata.csv'

    try:
        readUserFile = pd.read_csv(userFile)
    except:
        readUserFile = pd.DataFrame()

    phrase = input()
    if phrase == 'q':
        exit()
    sn = get_next_sn_by_user(username, readUserFile)
    print('sn =', str(sn), 'Your phrase is:', phrase)

    # Create New Session and Write To File
    kdf = pd.DataFrame(eventList, columns=['key', 'action', 'time'])
    readUserFile = addSNtoUser(username, readUserFile, kdf, phrase)
    readUserFile.to_csv('userdata.csv', index=False)


class KeyLogger(object):
    def __init__(self):
        self.enterPressed = False
        self.eventList = []
        self.initialized = False
        self.initialized2 = False

    def keyDownEvent(self, event):
        self.storeEvent("Down", event)
        return True
        # Fixes Requires Integer Bug (Got Nonetype)

    def keyUpEvent(self, event):
        self.storeEvent("Up", event)
        return True
        # Fixes Requires Integer (Got Nonetype)

    def mainLoop(self):
        while not self.enterPressed:
            pythoncom.PumpWaitingMessages()

    def storeEvent(self, activity, event):
        keystrokeTime = int(event.Time)
        # keystrokeCharacter = chr(event.Ascii)

        self.eventList.append((event.Key, activity, int(keystrokeTime)))

        # Chosen to use Escape key (ESC) due to input using a similar method
        # Enter Key - KeyCode: 13 Ascii: 13 ScanCode: 28 - ESC = 27 @ Ascii
        if not self.initialized:
            self.initialized = True
        elif event.Ascii == 13:  # 27:
            if not self.initialized2:
                self.initialized2 = True
            else:
                self.enterPressed = True
                self.eventList = [x for x in self.eventList if x[0] != 'Return']
                userRecordData(self.eventList)


def usernamePasswordInput():
    while True:
        keyLogger = KeyLogger()

        hookManager = pyHook.HookManager()
        hookManager.KeyDown = keyLogger.keyDownEvent
        hookManager.KeyUp = keyLogger.keyUpEvent
        hookManager.HookKeyboard()

        print('Type q to exit.')
        print('Enter your phrase: ')
        keyLogger.mainLoop()

        # Unhooks the keyboard, no more data recorded, returns to menu
        hookManager.UnhookKeyboard()


if __name__ == '__main__':
    getUserFileWriteSession()
    usernamePasswordInput()
