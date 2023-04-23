import requests
import sqlite3

import logging
formatter = '%(asctime)s : %(levelname)s : %(message)s'
logging.basicConfig(format=formatter, level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler('console.log')
handler.setFormatter(logging.Formatter(formatter))
logger.addHandler(handler)


def get_price_data(chart_sec, pair, before=0, after=0):
    
    params = {"periods": chart_sec}
    if before != 0:
        params["before"] = before
    if after != 0:
        params["after"] = after

    URL = f"https://api.cryptowat.ch/markets/bitflyer/{pair}/ohlc"
    response = requests.get(URL, params)

    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def create_table(connection):

    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_data (
            id INTEGER PRIMARY KEY,
            close_time INTEGER,
            chart_sec INTEGER,
            pair TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL,
            UNIQUE(close_time, pair) ON CONFLICT IGNORE
        )
    ''')
    connection.commit()

def save_to_sqlite(data, chart_sec, pair, connection):

    cursor = connection.cursor()
    inserted_nums = 0
    for entry in data["result"][str(chart_sec)]:
        cursor.execute('''
            INSERT OR IGNORE INTO price_data (close_time, chart_sec, pair, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (entry[0], chart_sec, pair, entry[1], entry[2], entry[3], entry[4], entry[5]))
        inserted_nums += cursor.rowcount
    connection.commit()

    return inserted_nums

def fetch_and_save_data():

    after = 1483228800
    chart_sec = 60
    pairs = ["btcjpy", "btcfxjpy"]
    db_file = "price_data.db"

    for pair in pairs:
        data = get_price_data(chart_sec, pair, after=after)
        if data:
            with sqlite3.connect(db_file) as connection:
                create_table(connection)
                inserted_nums = save_to_sqlite(data, chart_sec, pair, connection)
                logger.info(f"Inserted {inserted_nums} new rows for {pair} to {db_file}")
        else:
            logger.info(f"Failed to fetch price data for {pair}")

if __name__ == "__main__":

    fetch_and_save_data()