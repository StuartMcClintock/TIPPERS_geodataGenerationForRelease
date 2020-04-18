import sqlite3
import requests
import json
from buildDB import SPACETABLENAME

DEST_URL = 'https://dev-tippers.ics.uci.edu/api/entity/'
SOURCE_URL = 'https://dev-tippers.ics.uci.edu/api/entity/'

ID_OF_DESIRED_OBJ_TYPE = 7
ID_OF_PARENT_OBJ = 5

def getIdAndNameBuilding():
    data = requests.get(SOURCE_URL).json()
    nameDict = {}
    for datum in data:
        if datum["entityTypeId"] == ID_OF_PARENT_OBJ:
            nameDict[datum["name"]] = datum["id"]
    return nameDict

def getIdAndPair():
    data = requests.get(SOURCE_URL).json()
    nameDict = {}
    for datum in data:
        if datum["entityTypeId"] == ID_OF_DESIRED_OBJ_TYPE:
            nameDict[(datum["name"], datum["payload"]["geo"]["parentSpaceId"])] = datum["id"]
    return nameDict

def buildEntityObjects():
    con = sqlite3.connect('spaces.db')
    cursor = con.cursor()
    cursor.execute("SELECT space_id, space_name, floor_id, building_id FROM "+SPACETABLENAME+" WHERE space_type='Room';")
    subData = cursor.fetchall()
    
    cursor.execute("SELECT space_id, space_name, building_id FROM "+SPACETABLENAME+" WHERE space_type='Floor';")
    superData = cursor.fetchall()
    #print(superData)
    
    cursor.execute("SELECT space_id, space_name FROM "+SPACETABLENAME+" WHERE space_type='Building';")
    buildingData = cursor.fetchall()
    
    con.close()
    idMap = getIdAndPair()
    
    buildingNameMap = {}
    for building in buildingData:
        buildingNameMap[building[0]] = building[1]
    
    buildingIds = getIdAndNameBuilding()
    
    nameMap = {}
    for super in superData:
        try:
            nameMap[super[0]] = ('floor '+super[1], buildingIds[buildingNameMap[super[2]]])
        except KeyError:
            print("error with superspace "+str(super[0]))
    
    subObjects = []
    for subSpace in subData:
        newSubSpace = {}
        newSubSpace["name"] = "floor "+subSpace[1]
        newSubSpace["entityTypeId"] = ID_OF_DESIRED_OBJ_TYPE
        try:
            newSubSpace["payload"] = {"geo":{"parentSpaceId":idMap[nameMap[subSpace[2]]]}}
        except KeyError:
            continue
        subObjects.append(newSubSpace)
        
    return subObjects

def main():
    data = buildEntityObjects()
    for i in data:
        print(i)
    for datum in data:
        print(datum["name"])
        print(requests.post(DEST_URL, json=datum))
    
if (__name__=='__main__'):
    main()
