import sqlite3
import requests
import datetime
import pandas as pd 
import os

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

def get_ticket_info(teamID, venueID):
    url = f"https://api.stubhub.com/sellers/search/events/v3?venueId={venueID}&performerId={teamID}&parking=false&sort=eventDateLocal%20asc&rows=81"
    headers = { 
    "Authorization": "Bearer " + ACCESS_TOKEN,
    "Accept": "application/json"
    }
    r = requests.get(url, headers=headers)
    return r

def create_df(r):
    events = r.json()['events']
    prices = {event['id']:{
         "price": event['ticketInfo']['minPrice'],
         "time" : event['eventDateUTC'],
         "name" : event['name'],
         "extractTime":datetime.datetime.today(),
         "homeTeam" : event['performers'][0]['name'],
         "awayTeam" : event['performers'][1]['name']} for event in events}
    df = pd.DataFrame(prices).T.reset_index().rename({"index":"id"}, axis = 1)
    df['time'] = pd.to_datetime(df['time'].str[0:10])
    df['days_to_game'] = (df['time'] - df['extractTime'])
    df['days_to_game'] = df['days_to_game'].apply(lambda X: X.days)
    return df

def main():
    teams = {"Dodgers" : {"teamID": 1061, "venueID": 744},
         "Angels": {"teamID": 1062, "venueID" : 9763},
         "Giants" : {"teamID" : 197, "venueID" : 82}}
    for team in teams:
        teamID = teams[team]["teamID"]
        venueID = teams[team]["venueID"]
        r = get_ticket_info(teamID, venueID)
        df = create_df(r)
        with sqlite3.connect("tickets.db") as conn: 
            df.to_sql("extraction", conn, if_exists = "append", index = False)

if __name__ == "__main__":
    main()
