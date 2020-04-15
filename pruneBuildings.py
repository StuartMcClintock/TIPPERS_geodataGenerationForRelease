import sqlite3
import json
from buildDB import SPACETABLENAME

FILENAME  = 'buildingDataComplete.json'

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

def main():
    with open(FILENAME, 'r') as inF:
        oldBuildings = json.loads(inF.read())
        buildingInfo = removeUnnamed(oldBuildings)
    with open(FILENAME, 'w') as outF:
        json.dump(buildingInfo, outF)
        

if (__name__=='__main__'):
    main()
