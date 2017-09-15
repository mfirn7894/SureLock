
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# SETUP #
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import csv
from random import randint
from twilio.rest import TwilioRestClient
import serial
import time

arduino = serial.Serial('COM3', 115200, timeout=.1)

# Initialize Twilio API
ACCOUNT_SID = # user input
AUTH_TOKEN = # user input
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

# Specify CSV filepaths
doorCodeFilePath = # user input
lockerCodeFilePath = # user input
phoneDirectoryFilePath = # user input
twilioNumber = # user inpuut

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# DOOR CODE GENERATE #
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Read CSV file
def csvReaderDoor(fileName):
    with open(fileName, 'rU') as f:
        reader = csv.reader(f)
        codeListStr = list(reader)
        codeList = []
        for index in range(1, len(codeListStr)):
            codeList.append(int(codeListStr[index][0]))
        return codeList

# Delete valid code from CSV file
def codeRemoveDoor(filename, code):
    if code in csvReaderDoor(doorCodeFilePath):
        newList = csvReaderDoor(doorCodeFilePath)
        newList.remove(code)
        newList = ['Valid Codes'] + newList
        with open(filename, 'wb') as f:
            writer = csv.writer(f)
            for item in newList:
                writer.writerow([item, None])

# Check if code is valid
def codeValidateDoor(code, codeList):
    if code in codeList:
        print "Correct"
        arduino.write('Y')
        time.sleep(5)
        arduino.write('N')
        codeRemoveDoor(doorCodeFilePath, code)
        return
    else:
        print "Incorrect"
        return
    
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# LOCKER CODE GENERATE #
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Read CSV file
def csvReaderLocker1(fileName):
    with open(fileName, 'rU') as f:
        reader = csv.reader(f)
        codeListStr = list(reader)
        if codeListStr[0][0] == "Empty":
            validCode = "Empty"
        else:
            validCode = int(codeListStr[0][0])
        return validCode

# Write code to CSV
def csvWriterLocker(filename, code):
    with open(filename, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        data = code
        a.writerow([data, None])

# Read phone directory
phoneDict = {}
def phoneNum():
    reader = csv.reader(open(phoneDirectoryFilePath, 'rU'))
    for row in reader:
        k, v = row
        phoneDict[int(k)] = v
    return phoneDict

# Send text to resident
def textResident(apt, code):
    phoneDict = phoneNum()
    client.messages.create(to=phoneDict[apt], from_= twilioNumber, body= str("Your package has arrived! Enter code: "+ str(code)))
    print "Text message sent"
    
# Generate random code and store it in a dictionary in association with an apartment number
def getCodeLocker(apt):
    if type(csvReaderLocker1(lockerCodeFilePath)) == int:
        print "Locker already contains a package."
        return
    else:
        phoneDict = phoneNum()
        if apt in phoneDict:
            strCode = str(randint(1,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9)) + str(randint(0,9))
            code = int(strCode)
            # Tell Arduino to lock the door
            arduino.write('C')
            # Append to code CSV file
            csvWriterLocker(lockerCodeFilePath,code)
            textResident(apt, code)
            return code
        else:
            print "No apartment #",apt, "in this building."
            return
        
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# LOCKER CODE VALIDATE #
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Read CSV file
def csvReaderLocker2(fileName):
    with open(fileName, 'rU') as f:
        reader = csv.reader(f)
        codeListStr = list(reader)
        validCode = int(codeListStr[0][0])
        return validCode

# Delete valid code from CSV file
def codeRemoveLocker(filename, code):
    if code == csvReaderLocker2(lockerCodeFilePath):
        empty = ["Empty"]
        with open(filename, 'wb') as f:
            writer = csv.writer(f)
            for item in empty:
                writer.writerow([item, None])

# Check if code is valid
def codeValidateLocker(ardCode, validCode):
    if ardCode == validCode:
        print "Correct"
        arduino.write('O')
        codeRemoveLocker(lockerCodeFilePath, code)
        return
    else:
        print "Incorrect"
        return

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# EXECUTE #
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def codeDisplay(list1):
    newString = ""
    for item in list1:
        newString = newString+str(item)
    print "Code: " + newString
    if len(newString) == 3:
        print "Press '*' to submit apartment number"
    if len(newString) == 5:
        print "Press '*' to submit locker code"
    if len(newString) == 6:
        print "Press '*' to submit door code"


listy = []
while True:
    info = arduino.readline()[:-1]
    if info:
            if info == '#':
                    listy = []
            else:
                    listy.append(info)
                    codeDisplay(listy)
                    if len(listy)==7:
                            new_listy = listy[0:5]
                            if listy[6] == '*' and '*' not in new_listy:
                                    codeString = ""
                                    for index in range(0,6):
                                            codeString = codeString + listy[index]
                                            code = int(codeString)
                                    codeValidateDoor(code, csvReaderDoor(doorCodeFilePath))
                                    listy = []
                            else:
                                    listy = []
                    elif len(listy)==6:
                            new_listy = listy[0:4]
                            if listy[5] == '*' and '*' not in new_listy:
                                    codeString = ""
                                    for index in range(0,5):
                                            codeString = codeString + listy[index]
                                            code = int(codeString)
                                    codeValidateLocker(code, csvReaderLocker2(lockerCodeFilePath))
                                    listy = []
                    elif len(listy)==5:
                        continue
                    elif len(listy)==4:
                            new_listy = listy[0:2]
                            if listy[3] == '*' and '*' not in new_listy:
                                    aptString = ""
                                    for index in range(0,3):
                                            aptString = aptString + listy[index]
                                            apt = int(aptString)
                                    getCodeLocker(apt)
                                    listy = []
                    elif len(listy)==3 or len(listy)==2 or len(listy)==1:
                        continue
                    else:
                            listy = []

