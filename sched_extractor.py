import sqlite3
import requests
import datetime
import pandas as pd 

def get_ticket_info():
    url = "https://api.stubhub.com/sellers/search/events/v3?venueId=744&performerId=1061&parking=false&sort=eventDateLocal%20asc&rows=81"
    headers = { 
    "Authorization": "Bearer JA5o8vrYmwMO5akh50E4crz6i9XI",
    "Accept": "application/json"
    }
    r = requests.get(url, headers=headers)
    return r

def create_df(r):
    events = r.json()['events']
    prices = {event['id']: {"price": event['ticketInfo']['minPrice'], "time":event['eventDateLocal'], "name":event['name'], "extractTime":datetime.datetime.today()} for event in events}
    df = pd.DataFrame(prices).T.reset_index().rename({"index":"id"}, axis = 1)
    df['time'] = pd.to_datetime(df['time'].str[0:10])
    df['days_to_game'] = (df['time'] - df['extractTime'])
    df['days_to_game'] = df['days_to_game'].apply(lambda X: X.days)
    return df

def main():
    r = get_ticket_info()
    df = create_df(r)
    with sqlite3.connect("temps.db") as conn: 
        df.to_sql("extraction", conn, if_exists = "append", index = False)

if __name__ == "__main__":
    main()
