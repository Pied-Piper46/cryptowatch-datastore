import datetime
import sqlite3

def get_metadata_per_pair(connection, pairs):

    cursor = connection.cursor()
    metadata = {}

    for pair in pairs:

        cursor.execute("SELECT COUNT(*) FROM price_data WHERE pair=?", (pair,))
        total_count = cursor.fetchone()[0]

        cursor.execute("SELECT MIN(close_time), MAX(close_time) FROM price_data WHERE pair=?", (pair,))
        min_time, max_time = cursor.fetchone()

        min_date = datetime.datetime.fromtimestamp(min_time)
        max_date = datetime.datetime.fromtimestamp(max_time)
        
        metadata[pair] = {
            "total_count": total_count,
            "min_date": min_date,
            "max_date": max_date
        }

    return metadata

def show_metadata():

    pairs = ["btcjpy", "btcfxjpy"]
    with sqlite3.connect("price_data.db") as connection:
        metadata_per_pair = get_metadata_per_pair(connection, pairs)

        for pair, metadata in metadata_per_pair.items():
            print(f"Pair: {pair}")
            print(f"  Total data count: {metadata['total_count']}")
            print(f"  Data period: {metadata['min_date']} - {metadata['max_date']}")

if __name__ == "__main__":

    show_metadata()
