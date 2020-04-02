import sqlite3

con = sqlite3.connect('spaces.db')

cursor = con.cursor()

TABLENAME = 'neededSpaces'

def stripQuotes(val):
    val = val.replace('"', '')
    val = val.replace("'", '')
    return val

def getCompatibleValue(val):
    val = str(val)
    val = stripQuotes(val)
    if not val.isnumeric():
        return "'"+val+"'"
    return val

try:
    cursor.execute('''CREATE TABLE '''+TABLENAME+''' (
    space_id INTEGER PRIMARY KEY,
    space_name TEXT,
    space_type TEXT,
    building_id INTEGER,
    floor_id INTEGER);''')
except sqlite3.OperationalError:
    print('Table neededSpaces did not require creation, as it already exists')
    
with open('spaces_202003171129.csv') as csvFile:
    lines = csvFile.read().split('\n')
    firstLine = lines[0]
    lines = lines[1:]
    keyNames = firstLine.split(',')
    
    for line in lines:
        dataMap = {}
        lineKeys = []
        lineData = line.split(',')
        for i in range(0, len(lineData)):
            if lineData[i] != '':
                dataMap[keyNames[i]] = lineData[i]
                lineKeys.append(keyNames[i])
        
        if len(lineKeys) == 0:
            continue
    
        command = 'INSERT INTO '+TABLENAME+' ('+stripQuotes(lineKeys[0])
        for key in lineKeys[1:]:
            command += ','+stripQuotes(key)
        command += ') VALUES ('+getCompatibleValue(dataMap[lineKeys[0]])
        for key in lineKeys[1:]:
            command += ','+getCompatibleValue(dataMap[key])
        command += ');'
        try:
            cursor.execute(command)
        except sqlite3.IntegrityError:
            print('Element with id '+dataMap[lineKeys[0]]+' already exists. Skipping...')
        
        con.commit()
        

con.close()
