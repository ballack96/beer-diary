import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect('craft_beer.db')
cursor = conn.cursor()

# Create breweries table
cursor.execute('''
CREATE TABLE IF NOT EXISTS breweries (
    brewery_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT,
    state TEXT,
    country TEXT,
    latitude REAL,
    longitude REAL,
    website_url TEXT
)
''')

# Create beers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS beers (
    beer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    brewery_name TEXT,
    style TEXT,
    abv REAL,
    ibu INTEGER,
    description TEXT,
    country TEXT,
    image_url TEXT,
    rating REAL,
    added_on DATE DEFAULT CURRENT_DATE
)
''')

# Create tasting journal table
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasting_journal (
    journal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    beer_id TEXT,
    user_rating REAL,
    user_notes TEXT,
    tasted_on DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (beer_id) REFERENCES beers(beer_id)
)
''')

# Create favorites table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS favorite_breweries (
        fav_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        brewery_name TEXT,
        city TEXT,
        state TEXT,
        country TEXT,
        website_url TEXT
    )
''')

# Seed with some sample beers
sample_beers = [
    ("beer_001", "Pliny the Elder", "Russian River Brewing", "Double IPA", 8.0, 100, "Legendary hoppy Double IPA.", "USA", "", 4.7),
    ("beer_002", "Guinness Draught", "Guinness", "Stout", 4.2, 45, "Smooth and creamy classic Irish stout.", "Ireland", "", 4.3),
    ("beer_003", "Weihenstephaner Hefeweissbier", "Weihenstephan", "Hefeweizen", 5.4, 14, "World-class German wheat beer.", "Germany", "", 4.5),
    ("beer_004", "Saison Dupont", "Brasserie Dupont", "Saison", 6.5, 30, "Spicy and refreshing Belgian farmhouse ale.", "Belgium", "", 4.4),
    ("beer_005", "Sierra Nevada Pale Ale", "Sierra Nevada Brewing", "Pale Ale", 5.6, 38, "The classic American pale ale.", "USA", "", 4.2),
]

cursor.executemany('''
INSERT OR IGNORE INTO beers (beer_id, name, brewery_name, style, abv, ibu, description, country, image_url, rating)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', sample_beers)

# Insert sample breweries
sample_breweries = [
    ("brewery_001", "Russian River Brewing", "Santa Rosa", "California", "USA", 38.4405, -122.7144, "https://www.russianriverbrewing.com/"),
    ("brewery_002", "Sierra Nevada Brewing", "Chico", "California", "USA", 39.7285, -121.8375, "https://sierranevada.com/"),
    ("brewery_003", "Guinness Storehouse", "Dublin", "Leinster", "Ireland", 53.3419, -6.2866, "https://www.guinness-storehouse.com/")
]

cursor.executemany('''
INSERT OR IGNORE INTO breweries (brewery_id, name, city, state, country, latitude, longitude, website_url)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', sample_breweries)

conn.commit()
conn.close()

print("✅ Database initialized and sample beers inserted!")
