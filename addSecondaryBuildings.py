import json
import sqlite3
from buildDB import SPACETABLENAME

FILENAME = 'buildingDataComplete.json'

def removeExtraData(building):
    rmKeys = ["id", "entityClassId", "entityClassName", "entityTypeName"]
    for k in rmKeys:
        try:
            del building[k]
        except KeyError:
            pass
    return building

def addNewFromJSON(data):
    with open('additionalBuildings.json', 'r') as newBuildingFile:
        newBuildings = json.load(newBuildingFile)
    
    currentNames = []
    for building in data:
        currentNames.append(building["name"])
    
    for building in newBuildings:
        if not building["name"] in currentNames:
            currentNames.append(building["name"])
            building = removeExtraData(building)
            data.append(building)
    
    return data
        
    
def addNewFromDB(data):
    return data

def main():
    with open(FILENAME, 'r') as inF:
        data = json.load(inF)
        data = addNewFromJSON(data)
        data = addNewFromDB(data)
        
    with open(FILENAME, 'w') as outF:
        json.dump(data, outF)
    print(type(data), data)
    
if (__name__=='__main__'):
    main()
