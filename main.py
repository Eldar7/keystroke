import pyHook
import pythoncom
import json
import os
import pandas as pd

# File is to be opened and closed numerous times. Should be re-written as a class.
global userFilePath


def getUserFileWriteSession():

    print("File Location: ", os.getcwd())
    username = 'user'#input("Enter your username: ")
    userFileName = (username + ".txt")

    # If directory DNE.
    if not os.path.isdir((os.path.join("./", "accounts"))):
        # Create it.
        os.makedirs("accounts")

    if os.path.exists(os.path.join("accounts", userFileName)):
        userFile = (os.path.join("accounts", userFileName))
    else:
        print("No File Exists! Creating New User")
        if os.path.exists(os.path.join("accounts", userFileName)):
            print("Username exists! Load it or choose different name")
        else:
            userFile = (os.path.join("accounts", userFileName))
            writeFile = open(userFile, "w")
            # Have to prime a file ready to be used with JSON
            fileSetup = json.dumps([])
            writeFile.write(fileSetup)
            writeFile.close()
            print("User Successfully Created", userFile)
    print("Your account has been created: ", userFile)

    global userFilePath
    userFilePath = userFile


def get_next_sn_by_user(username, df):
    try:
        next_sn = max(df[df.username == username].sn) + 1
    except:
        next_sn = 0
    return next_sn


def addSNtoUser(username, df, dfToAdd):
    sn = get_next_sn_by_user(username, df)
    dftmp = pd.DataFrame([[username, sn]], columns=['username', 'sn'])

    ndf = pd.DataFrame()
    ndf = ndf.append(dftmp).join(dfToAdd, how='right')

    ndf.username = ndf.username.fillna(username)
    ndf.sn = ndf.sn.fillna(sn)

    return pd.concat([df, ndf], ignore_index=True)


def userRecordData(eventList):
    userFile = 'userdata.csv'

    try:
        readUserFile = pd.read_csv(userFile)
    except:
        readUserFile = pd.DataFrame()

    # Create New Session and Write To File
    kdf = pd.DataFrame(eventList, columns=['key', 'action', 'time'])
    readUserFile = addSNtoUser('user1', readUserFile, kdf)
    readUserFile.to_csv('userdata.csv', index=False)


class KeyLogger(object):
    def __init__(self):
        self.enterPressed = False
        self.eventList = []
        self.initialized = False

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
        #keystrokeCharacter = chr(event.Ascii)

        self.eventList.append((event.Key, activity, int(keystrokeTime)))

        # Chosen to use Escape key (ESC) due to input using a similar method
        # Enter Key - KeyCode: 13 Ascii: 13 ScanCode: 28 - ESC = 27 @ Ascii
        if not self.initialized:
            self.initialized = True
        elif event.Ascii == 13:#27:
            self.enterPressed = True
            del self.eventList[0]#Удалим отпускание Enter, которое почему-то записывается
            del self.eventList[-1]#Удалим нажатие Enter в конце
            userRecordData(self.eventList)


def usernamePasswordInput():

    keyLogger = KeyLogger()

    hookManager = pyHook.HookManager()
    hookManager.KeyDown = keyLogger.keyDownEvent
    hookManager.KeyUp = keyLogger.keyUpEvent
    hookManager.HookKeyboard()

    print('here we go')
    keyLogger.mainLoop()

    # Unhooks the keyboard, no more data recorded, returns to menu
    hookManager.UnhookKeyboard()


if __name__ == '__main__':
    getUserFileWriteSession()

    usernamePasswordInput()