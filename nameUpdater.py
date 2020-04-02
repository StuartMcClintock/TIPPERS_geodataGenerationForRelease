import sqlite3
from buildDB import SPACETABLENAME
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

INPUT_FILE = 'buildingDataOriginal.json'
OUTPUT_FILE  = 'buildingDataNew.json'

def findCorrectName(name):
    con = sqlite3.connect('spaces.db')
    cursor = con.cursor()
    cursor.execute('SELECT * FROM '+SPACETABLENAME+" WHERE space_name='"+name+"'")
    info = cursor.fetchall()
    con.close()
    if len(info) == 1:
        return name
    return 'holder'

with open(INPUT_FILE, 'r') as inpt, open(OUTPUT_FILE, 'w') as outpt:
    inptLine = inpt.readline()
    while inptLine != '':
        if '"name"' in inptLine:
            splitList = inptLine.split('"')
            currentName = splitList[3]
            newName = findCorrectName(currentName)
            splitList[3] = newName
            newLine = '"'.join(splitList)
            outpt.write(newLine)
        else:
            outpt.write(inptLine)
        
        inptLine = inpt.readline()
