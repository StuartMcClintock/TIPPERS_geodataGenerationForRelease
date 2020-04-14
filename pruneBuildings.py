import sqlite3
import json
from buildDB import SPACETABLENAME

INPUT_FILE = 'buildingDataUpdated.json'
OUTPUT_FILE  = 'buildingDataComplete.json'

def removeUnnamed(buildingInfo):
    con = sqlite3.connect('spaces.db')
    cursor = con.cursor()
    cursor.execute('SELECT space_name FROM '+SPACETABLENAME+" WHERE space_type='Building';")
    namedBuildings = cursor.fetchall()
    con.close()
    
    namedBuildings = [i[0] for i in namedBuildings]
    
    delList = []
    index = 0
    for building in buildingInfo:
        if not building['name'] in namedBuildings:
            delList.append(index)
        index+=1
    delList.reverse()
    for i in delList:
        del buildingInfo[i]
        
    return buildingInfo

with open(INPUT_FILE, 'r') as inF, open(OUTPUT_FILE, 'w') as outF:
    oldBuildings = json.loads(inF.read())
    buildingInfo = removeUnnamed(oldBuildings)
    json.dump(buildingInfo, outF)
    
    
