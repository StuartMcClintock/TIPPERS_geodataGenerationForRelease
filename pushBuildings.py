import requests
import json

INPUT_FILE = 'buildingDataComplete.json'
DEST_URL = 'https://dev-tippers.ics.uci.edu/api/entity/'

with open(INPUT_FILE, 'r') as f:
    data = json.load(f)

req = requests.get(DEST_URL)
preexistingEntities = json.loads(req.text)
takenNames = []
for ent in preexistingEntities:
    takenNames.append(ent["name"])

for datum in data:
    if not datum["name"] in takenNames:
        print('POST request to add '+datum['name']+'...')
        try:
            print(requests.post(DEST_URL, json=datum))
        except:
            newData = datum
            newData["payload"] = {"geo":{"parentSpaceId":10000}}
            print(requests.post(DEST_URL, json=newData))
