import sqlite3
import requests
import json
from buildDB import SPACETABLENAME;

SOURCE_URL = 'https://dev-tippers.ics.uci.edu/api/entity/'

def getIdAndName():
    data = requests.get(SOURCE_URL).json()
    nameDict = {}
    for datum in data:
        nameDict[datum["name"]] = datum["id"]
    return nameDict
    
def main():
    apiIds = getIdAndName()
    con = sqlite3.connect('spaces.db')
    cursor = con.cursor()
    for name in apiIds.keys():
        cursor.execute("UPDATE "+SPACETABLENAME+" SET apiId="+str(apiIds[name])+" WHERE space_name='"+name+"'")
        print(name, "has been set to", apiIds[name])
    con.close()
    
if __name__=='__main__':
    main()
