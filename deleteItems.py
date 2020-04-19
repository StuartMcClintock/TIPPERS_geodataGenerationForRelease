import requests

DEST_URL = 'https://dev-tippers.ics.uci.edu/api/entity/'
START_ID = 13775
END_ID = 13989


def main():
    for entityId in range(START_ID, END_ID+1):
        print(entityId)
        print(requests.delete(DEST_URL+str(entityId)))


if __name__ == '__main__':
    main()
