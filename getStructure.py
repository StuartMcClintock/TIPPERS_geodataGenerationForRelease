import csv, requests

CSV_NAME = 'currentSpaces.csv'
SOURCE_URL = 'https://dev-tippers.ics.uci.edu/api/entity/'

BUILDING_TYPE_ID = 5
FLOOR_TYPE_ID = 7
REGION_TYPE_ID = 12


def main():
    data = requests.get(SOURCE_URL, params={"limit":3000}).json()
    
    indexedData = {}
    for datum in data:
        indexedData[datum["id"]] = datum
    with open(CSV_NAME, 'w', newline='') as outFile:
        writer = csv.writer(outFile)
        writer.writerow(["id", "name", "buildingId", "floorId"])
        for datum in data:
            row = [datum["id"], datum["name"], None, None]
            if datum["entityTypeId"] == FLOOR_TYPE_ID:
                row[2] = datum["payload"]["geo"]["parentSpaceId"]
            elif datum["entityTypeId"] == REGION_TYPE_ID:
                row[3] = datum["payload"]["geo"]["parentSpaceId"]
                row[2] = indexedData[datum["payload"]["geo"]["parentSpaceId"]]["payload"]["geo"]["parentSpaceId"]
            if datum["entityTypeId"] in (BUILDING_TYPE_ID, FLOOR_TYPE_ID, REGION_TYPE_ID):
                writer.writerow(row)
        
    
if __name__=='__main__':
    main()
