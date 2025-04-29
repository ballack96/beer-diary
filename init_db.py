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

# Create tasting journal table if it doesn't exist
cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasting_journal (
            journal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            beer_id TEXT,
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

# Create Beers Catalog Table if it doesn't exist
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


# --- Load and Preprocess Beer Dataset ---
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

# --- Insert into beers_catalog Table ---
cursor.execute('DELETE FROM beers_catalog')  # Clear old entries if any
for _, row in df.iterrows():
    cursor.execute('''
    INSERT INTO beers_catalog (beer_name, brewery_name, style, abv, ibu, description)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (row['beer_name'], row['brewery_name'], row['style'], row['abv'], row['ibu'], row['description']))

conn.commit()
conn.close()

print("✅ Database initialized and sample beers inserted!")
