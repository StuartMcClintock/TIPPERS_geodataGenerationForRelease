import sqlite3
import requests
import json
from buildDB import SPACETABLENAME

DEST_URL = 'https://dev-tippers.ics.uci.edu/api/entity/'
SOURCE_URL = 'https://dev-tippers.ics.uci.edu/api/entity/'

def getIdAndName():
    data = requests.get(SOURCE_URL).json()
    nameDict = {}
    for datum in data:
        nameDict[datum["name"]] = datum["id"]
    return nameDict

def buildFloorObjects():
    con = sqlite3.connect('spaces.db')
    cursor = con.cursor()
    cursor.execute("SELECT space_id, space_name, building_id FROM "+SPACETABLENAME+" WHERE space_type='Floor';")
    floorData = cursor.fetchall()
    cursor.execute("SELECT space_id, space_name FROM "+SPACETABLENAME+" WHERE space_type='Building';")
    nameList = cursor.fetchall()
    con.close()
    idMap = getIdAndName()
    
    nameMap = {}
    for building in nameList:
        nameMap[building[0]] = building[1]
    
    #print(nameMap)
    #print(idMap)
    
    floorObjects = []
    for floor in floorData:
        newFloor = {}
        newFloor["name"] = "floor "+floor[1]
        newFloor["entityTypeId"] = 7
        try:
            newFloor["payload"] = {"geo":{"parentSpaceId":idMap[nameMap[floor[2]]]}}
        except KeyError:
            continue
        floorObjects.append(newFloor)
        
    return floorObjects

def main():
    data = buildFloorObjects()
    print(data)
    for datum in data:
        print(datum["name"])
        print(requests.post(DEST_URL, json=datum))
    
if (__name__=='__main__'):
    main()
