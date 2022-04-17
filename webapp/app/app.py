import time
from flask import Flask
import pandas as pd
import sqlite3
app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': time.time()} 

@app.route('/df')
def get_data_frame():
    with sqlite3.connect("../../tickets.db") as conn: 
        cmd = \
            """
            SELECT g.*, e.price, e.extractTime, e.ticket_count FROM extraction e
            LEFT JOIN games g on e.id = g.id
            WHERE g.season = 2022
            """
        df = pd.read_sql_query(cmd, conn)
    df['time'], df['extractTime'] = pd.to_datetime(df['time']), pd.to_datetime(df['extractTime'])
    df['days_to_game'] = (df['time'] - df['extractTime'])
    df['days_to_game'] = df['days_to_game'].apply(lambda X: X.days)
    df = df.dropna()
    def diff_from_max(x):
        initial = x.to_numpy()[0]
        return (initial - x)/x
    df["diff_initial"] = df.groupby("unique_name")["price"].transform(diff_from_max)
    df = df[df['extractTime'] > '2022-03-01']
    return {"length": len(df)}