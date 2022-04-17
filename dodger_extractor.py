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
         "extractTime": datetime.datetime.today(),
         "ticket_count": event["ticketInfo"]["totalTickets"]} for event in events}
    df = pd.DataFrame(prices).T.reset_index().rename({"index":"id"}, axis = 1)
    return df

teams = {"Dodgers" : {"teamID": 1061, "venueID": 744}}

def main():
    for team in teams:
        teamID = teams[team]["teamID"]
        venueID = teams[team]["venueID"]
        r = get_ticket_info(teamID, venueID)
        df = create_df(r)
        with sqlite3.connect("tickets.db") as conn: 
            df.to_sql("dodger_extraction", conn, if_exists = "append", index = False)

if __name__ == "__main__":
    main()
