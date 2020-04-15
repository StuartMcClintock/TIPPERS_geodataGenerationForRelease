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

def convertGPS(verticies):
    newVerticies = []
    for point in verticies:
        point['latitude'] = float(point['latitude'])
        point['longitude'] = float(point['longitude'])
        newVerticies.append(point)
    return newVerticies

def addNewFromJSON(data):
    with open('additionalBuildings.json', 'r') as newBuildingFile:
        newEntities = json.load(newBuildingFile)
    
    currentNames = []
    for building in data:
        currentNames.append(building["name"])
    
    for entity in newEntities:
        if not entity["name"] in currentNames and entity["entityTypeId"]==5:
            currentNames.append(entity["name"])
            entity = removeExtraData(entity)
            try:
                entity['payload']['geo']['extent']['verticies'] = convertGPS(building['payload']['geo']['extent']['verticies'])
            except KeyError:
                print('Encountered building without geodata. Proceeding without it...')
            data.append(entity)
    
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
    
if (__name__=='__main__'):
    main()
