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

teams = {"Diamondbacks" : {"teamID": 701, "venueID": 365},
         "Braves" : {"teamID": 5643, "venueID": 447274},
         "Cubs": {"teamID": 5644, "venueID": 4207},
         "Reds": {"teamID": 4862, "venueID": 5844},
         "Rockies": {"teamID": 5646, "venueID": 4205},
         "Marlins": {"teamID": 4342, "venueID": 194876},
         "Brewers": {"teamID": 5164, "venueID": 3626},
         "Phillies": {"teamID": 4344, "venueID": 9563},
         "Mets": {"teamID": 5649, "venueID": 139704},
         "Pirates": {"teamID": 4802, "venueID": 3241},
         "Cardinals": {"teamID": 5651, "venueID": 4161},
         "Padres": {"teamID": 581, "venueID": 9643},
         "Nationals": {"teamID": 7547, "venueID": 108502},
         "Orioles": {"teamID": 4962, "venueID": 3401},
         "Red Sox": {"teamID": 4322, "venueID": 2901},
         "White Sox": {"teamID": 5645, "venueID": 4208},
         "Guardians": {"teamID": 4882, "venueID": 3262},
         "Tigers": {"teamID": 4182, "venueID": 2741},
         "Astros": {"teamID": 4782, "venueID": 3221},
         "Royals": {"teamID": 5647, "venueID": 4221},
         "Twins": {"teamID": 5648, "venueID": 141505},
         "Yankees": {"teamID": 5650, "venueID": 4222},
         "A's": {"teamID": 198, "venueID": 83},
         "Mariners": {"teamID": 1043, "venueID": 763},
         "Rays": {"teamID": 5652, "venueID": 4211},
         "Rangers": {"teamID": 4343, "venueID": 102150041},
         "Dodgers" : {"teamID": 1061, "venueID": 744},
         "Angels": {"teamID": 1062, "venueID" : 9763},
         "Giants" : {"teamID" : 197, "venueID" : 82}}

def main():
    for team in teams:
        teamID = teams[team]["teamID"]
        venueID = teams[team]["venueID"]
        r = get_ticket_info(teamID, venueID)
        df = create_df(r)
        with sqlite3.connect("tickets.db") as conn: 
            df.to_sql("extraction", conn, if_exists = "append", index = False)

if __name__ == "__main__":
    main()
