import os
import sqlite3
import pandas as pd

def initialize_database_if_needed():
    # # Delete old db
    # if os.path.exists('craft_beer.db'):
    #     os.remove('craft_beer.db')

    conn = sqlite3.connect('craft_beer.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS beers_catalog (
        beer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        beer_name TEXT,
        brewery_name TEXT,
        style TEXT,
        abv REAL,
        ibu REAL,
        description TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasting_journal (
        journal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        beer_id TEXT,
        brewery_name TEXT,
        look REAL,
        smell REAL,
        taste REAL,
        feel REAL,
        overall REAL,
        average_rating REAL,
        user_notes TEXT,
        tasted_on DATE DEFAULT CURRENT_DATE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS favorite_breweries (
        fav_id INTEGER PRIMARY KEY AUTOINCREMENT,
        brewery_name TEXT,
        city TEXT,
        state TEXT,
        country TEXT,
        website_url TEXT,
        user_id TEXT
    )
    ''')

    # Load beers from CSV
    df = pd.read_csv('beer_data_set.csv')
    df = df[["Name", "Brewery", "Style", "ABV", "Min IBU", "Max IBU", "Description"]]
    df = df.rename(columns={
        "Name": "beer_name",
        "Brewery": "brewery_name",
        "Style": "style",
        "ABV": "abv",
        "Description": "description"
    })
    df['ibu'] = (df['Min IBU'].fillna(0) + df['Max IBU'].fillna(0)) / 2
    df = df.drop(columns=["Min IBU", "Max IBU"])
    df['abv'] = df['abv'].fillna(0)
    df['ibu'] = df['ibu'].fillna(0)
    df['description'] = df['description'].fillna('No description available.')

    for _, row in df.iterrows():
        cursor.execute('''
        INSERT INTO beers_catalog (beer_name, brewery_name, style, abv, ibu, description)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (row['beer_name'], row['brewery_name'], row['style'], row['abv'], row['ibu'], row['description']))

    conn.commit()
    conn.close()

    print("✅ Database initialized on startup.")

