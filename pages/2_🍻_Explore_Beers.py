import streamlit as st
import sqlite3
import pandas as pd
import requests

# ------------------------------
# Database connection
# ------------------------------
def get_connection():
    return sqlite3.connect('craft_beer.db')

# Insert tasting journal entry
def add_to_journal(user_id, beer_name, user_rating, user_notes):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tasting journal table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasting_journal (
            journal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            beer_id TEXT,
            user_rating REAL,
            user_notes TEXT,
            tasted_on DATE DEFAULT CURRENT_DATE
        )
    ''')

    # Since live beers from API won't have static beer_id, we use beer_name as beer_id
    beer_id = beer_name

    cursor.execute('''
        INSERT INTO tasting_journal (user_id, beer_id, user_rating, user_notes)
        VALUES (?, ?, ?, ?)
    ''', (user_id, beer_id, user_rating, user_notes))
    conn.commit()
    conn.close()

# Fetch beers from Punk API
@st.cache_data
def load_beers():
    df = pd.read_csv('beer_data_set.csv')
    # Select and rename necessary columns
    df = df[["Name", "Brewery", "Style", "ABV", "Min IBU", "Max IBU", "Description"]]
    df = df.rename(columns={
        "Name": "beer_name",
        "Brewery": "brewery_name",
        "Style": "style",
        "ABV": "abv",
        "Description": "description"
    })
    # Compute average IBU
    df['ibu'] = (df['Min IBU'].fillna(0) + df['Max IBU'].fillna(0)) / 2
    df = df.drop(columns=["Min IBU", "Max IBU"])
    # Fill missing values
    df['abv'] = df['abv'].fillna(0)
    df['ibu'] = df['ibu'].fillna(0)
    df['description'] = df['description'].fillna('No description available.')
    return df


# ------------------------------
# Streamlit Page
# ------------------------------
st.title("🍻 Explore Beers (Kaggle Dataset)")

beers_df = load_beers()

if beers_df.empty:
    st.warning("No beers found.")
else:
    # --- Sidebar Filters ---
    st.sidebar.header("🔎 Filters")

    # Style Dropdown Filter
    all_styles = sorted(beers_df['style'].dropna().unique())
    selected_style = st.sidebar.selectbox(
        "Select Beer Style", 
        ["All Styles"] + all_styles
    )

    # Search bar
    search_term = st.text_input("🔍 Search for a beer by name...")

    # --- Filter DataFrame ---
    filtered_beers = beers_df.copy()

    if selected_style != "All Styles":
        filtered_beers = filtered_beers[filtered_beers['style'] == selected_style]

    if search_term:
        filtered_beers = filtered_beers[filtered_beers['beer_name'].str.contains(search_term, case=False)]

    st.write(f"Showing {len(filtered_beers)} beers:")

    # --- Show Beers ---
    for idx, row in filtered_beers.iterrows():
        st.markdown("---")
        st.markdown(f"### 🍺 {row['beer_name']}")
        st.markdown(f"**Brewery:** {row['brewery_name']}")
        st.markdown(f"**Style:** {row['style']}")
        st.markdown(f"**ABV:** {row['abv']}% | **IBU:** {row['ibu']}")
        st.markdown(f"**Description:** {row['description']}")

        with st.expander("➕ Add to Tasting Journal"):
            rating = st.slider(f"Rate {row['beer_name']} (0-5)", 0.0, 5.0, 3.0, step=0.1, key=f"rating_{idx}")
            notes = st.text_area(f"Your notes on {row['beer_name']}", key=f"notes_{idx}")
            if st.button(f"Save {row['beer_name']}", key=f"save_{idx}"):
                add_to_journal(user_id="guest", beer_name=row['beer_name'], user_rating=rating, user_notes=notes)
                st.success(f"Saved {row['beer_name']} to your Tasting Journal! 🍻")
