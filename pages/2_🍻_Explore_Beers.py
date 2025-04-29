import streamlit as st
import sqlite3
import pandas as pd
import requests

# ------------------------------
# Database connection
# ------------------------------
def get_connection():
    return sqlite3.connect('craft_beer.db')

# Load beers from database
@st.cache_data
def load_beers():
    conn = get_connection()
    df = pd.read_sql_query('SELECT * FROM beers_catalog', conn)
    conn.close()
    return df

# Save tasting journal with composite rating
def add_to_journal(user_id, beer_name, look, smell, taste, feel, overall, notes):
    conn = get_connection()
    cursor = conn.cursor()

    avg_rating = (look + smell + taste + feel + overall) / 5

    beer_id = beer_name

    cursor.execute('''
        INSERT INTO tasting_journal (user_id, beer_id, look, smell, taste, feel, overall, average_rating, user_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, beer_id, look, smell, taste, feel, overall, avg_rating, notes))
    conn.commit()
    conn.close()

# ------------------------------
# Streamlit Page
# ------------------------------
st.title("🍻 Explore Beers (Database Loaded)")

beers_df = load_beers()

if beers_df.empty:
    st.warning("No beers found.")
else:
    # Sidebar Filters
    st.sidebar.header("🔎 Filters")

    # Style Dropdown
    all_styles = sorted(beers_df['style'].dropna().unique())
    selected_style = st.sidebar.selectbox(
        "Select Beer Style",
        ["All Styles"] + all_styles
    )

    # ABV Slider
    abv_min = float(beers_df['abv'].min())
    abv_max = float(beers_df['abv'].max())
    selected_abv = st.sidebar.slider("Select ABV Range (%)", abv_min, abv_max, (abv_min, abv_max))

    # Search bar
    search_term = st.text_input("🔍 Search for a beer by name...")

    # Filtering
    filtered_beers = beers_df.copy()

    if selected_style != "All Styles":
        filtered_beers = filtered_beers[filtered_beers['style'] == selected_style]

    filtered_beers = filtered_beers[
        (filtered_beers['abv'] >= selected_abv[0]) & (filtered_beers['abv'] <= selected_abv[1])
    ]

    if search_term:
        filtered_beers = filtered_beers[filtered_beers['beer_name'].str.contains(search_term, case=False)]

    st.write(f"Showing {len(filtered_beers)} beers:")

    for idx, row in filtered_beers.iterrows():
        st.markdown("---")
        st.markdown(f"### 🍺 {row['beer_name']}")
        st.markdown(f"**Brewery:** {row['brewery_name']}")
        st.markdown(f"**Style:** {row['style']}")
        st.markdown(f"**ABV:** {row['abv']}% | **IBU:** {row['ibu']}")
        st.markdown(f"**Description:** {row['description']}")

        with st.expander("➕ Add to Tasting Journal"):
            look = st.slider(f"Look (0-5)", 0.0, 5.0, 3.0, step=0.5, key=f"look_{idx}")
            smell = st.slider(f"Smell (0-5)", 0.0, 5.0, 3.0, step=0.5, key=f"smell_{idx}")
            taste = st.slider(f"Taste (0-5)", 0.0, 5.0, 3.0, step=0.5, key=f"taste_{idx}")
            feel = st.slider(f"Feel (0-5)", 0.0, 5.0, 3.0, step=0.5, key=f"feel_{idx}")
            overall = st.slider(f"Overall (0-5)", 0.0, 5.0, 3.0, step=0.5, key=f"overall_{idx}")
            notes = st.text_area(f"Your notes on {row['beer_name']}", key=f"notes_{idx}")
            if st.button(f"Save {row['beer_name']}", key=f"save_{idx}"):
                add_to_journal(user_id="guest", beer_name=row['beer_name'], look=look, smell=smell, taste=taste, feel=feel, overall=overall, notes=notes)
                st.success(f"Saved {row['beer_name']} to your Tasting Journal! 🍻")
