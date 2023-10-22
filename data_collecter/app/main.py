import requests
import sqlite3
import traceback
import logging
import logging.handlers
from config import DATABASE_URL, EMAIL_ADDR, EMAIL_PASS

def setup_logger():

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # handler = logging.FileHandler('logs/console.log')
    handler = logging.handlers.SMTPHandler(
        mailhost=("smtp.gmail.com", 587),
        fromaddr=EMAIL_ADDR,
        toaddrs=[EMAIL_ADDR],
        subject="Cryptowatch data gathering",
        credentials=(EMAIL_ADDR, EMAIL_PASS),
        secure=()
    )

    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_price_data(pair):
    
    params = {"fsym": "BTC", "tsym": "JPY", "e": pair, "limit": 2000}

    endpoint = f"https://min-api.cryptocompare.com/data/histominute"
    response = requests.get(endpoint, params, timeout=10)

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
    
    for entry in data["Data"][:-1]:
        cursor.execute('''
            INSERT OR IGNORE INTO price_data (close_time, chart_sec, pair, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (entry['time'], chart_sec, pair, entry['open'], entry['high'], entry['low'], entry['close'], entry['volumefrom']))
        inserted_nums += cursor.rowcount
    connection.commit()

    return inserted_nums


def fetch_and_save_data(logger):

    try:
        chart_sec = 60
        pairs = ["bitflyer", "bitflyerfx"]
        db_path = "../.." + DATABASE_URL

        for pair in pairs:
            data = get_price_data(pair)
            if data:
                with sqlite3.connect(db_path) as connection:
                    create_table(connection)
                    inserted_nums = save_to_sqlite(data, chart_sec, pair, connection)
                    logger.info(f"Inserted {inserted_nums} new rows for {pair} to {db_path}")
            else:
                logger.info(f"Failed to fetch price data for {pair}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    logger = setup_logger()
    fetch_and_save_data(logger)