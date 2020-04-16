import requests
import json

INPUT_FILE = 'buildingDataComplete.json'
DEST_URL = 'http://dev-tippers.ics.uci.edu/api/entity/'

with open(INPUT_FILE, 'r') as f:
    data = json.load(f)

for datum in data:
    print(requests.post(DEST_URL, json=datum))
