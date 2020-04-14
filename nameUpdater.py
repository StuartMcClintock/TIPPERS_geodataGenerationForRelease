import sqlite3
from buildDB import SPACETABLENAME

INPUT_FILE = 'buildingDataOriginal.json'
OUTPUT_FILE  = 'buildingDataUpdated.json'

def displayOptions():
    con = sqlite3.connect('spaces.db')
    cursor = con.cursor()
    cursor.execute('SELECT space_id, space_name FROM '+SPACETABLENAME+" WHERE space_type='Building';")
    data = cursor.fetchall()
    
    for datum in data:
        print(datum[0],'|',datum[1])
    
    con.close();

def findCorrectName(name):
    con = sqlite3.connect('spaces.db')
    cursor = con.cursor()
    cursor.execute('SELECT space_name FROM '+SPACETABLENAME+" WHERE space_name='"+name+"';")
    info = cursor.fetchall()
    
    if len(info) == 1:
        con.close()
        return name
    
    while len(info)==0:
        print(name)
        givenID = input("ID of corresponding building name: ")
        if (givenID == ''):
            return name
        if givenID == 'quit':
            return 'quit'
        cursor.execute('SELECT space_name FROM '+SPACETABLENAME+" WHERE space_id='"+givenID+"';")
        info = cursor.fetchall()
    
    return info[0][0]
    
    con.close()
    return 'holder'

with open(INPUT_FILE, 'r') as inpt, open(OUTPUT_FILE, 'w') as outpt:
    displayOptions()
    
    terminateMode = False
    
    inptLine = inpt.readline()
    while inptLine != '':
        if '"name"' in inptLine and not terminateMode:
            splitList = inptLine.split('"')
            currentName = splitList[3]
            newName = findCorrectName(currentName)
            if newName=='quit':
                terminateMode = True
                continue
            splitList[3] = newName
            newLine = '"'.join(splitList)
            outpt.write(newLine)
        else:
            outpt.write(inptLine)
        
        inptLine = inpt.readline()

with open(OUTPUT_FILE, 'r') as inpt, open(INPUT_FILE, 'w') as outpt:
    outpt.write(inpt.read())
