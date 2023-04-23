import json
import sqlite3
import main

def load_json_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def migrate_json_to_sqlite(json_filename, sqlite_filename, pair):
    
    chart_sec = 60
    json_data = load_json_data(json_filename)

    with sqlite3.connect(sqlite_filename) as connection:
        main.create_table(connection)
        main.save_to_sqlite(json_data, chart_sec, pair, connection)

if __name__ == "__main__":

    migrate_json_to_sqlite('/Users/yuji/Documents/BATMAN/data_fx.json', 'price_data.db', 'btcfxjpy')