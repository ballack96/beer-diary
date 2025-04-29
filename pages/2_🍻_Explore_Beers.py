import streamlit as st
import sqlite3
import pandas as pd

def get_connection():
    return sqlite3.connect('craft_beer.db')

def load_beers():
    conn = get_connection()
    beers_df = pd.read_sql_query("SELECT * FROM beers", conn)
    conn.close()
    return beers_df

def add_to_journal(user_id, beer_id, user_rating, user_notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasting_journal (user_id, beer_id, user_rating, user_notes)
        VALUES (?, ?, ?, ?)
    """, (user_id, beer_id, user_rating, user_notes))
    conn.commit()
    conn.close()

st.title("🍻 Explore Beers")

beers = load_beers()

search_term = st.text_input("Search for a beer...")
style_filter = st.selectbox("Filter by Style", ["All"] + sorted(beers['style'].dropna().unique().tolist()))

filtered_beers = beers
if search_term:
    filtered_beers = filtered_beers[filtered_beers['name'].str.contains(search_term, case=False)]
if style_filter != "All":
    filtered_beers = filtered_beers[filtered_beers['style'] == style_filter]

st.dataframe(filtered_beers)

st.markdown("---")
st.subheader("Add to Your Tasting Journal")

beer_options = filtered_beers['name'].tolist()
selected_beer = st.selectbox("Select a beer to add", beer_options)

rating = st.slider("Your Rating (0-5)", 0.0, 5.0, 3.0, step=0.1)
notes = st.text_area("Your Tasting Notes")

if st.button("Save to Journal"):
    beer_id = beers[beers['name'] == selected_beer]['beer_id'].values[0]
    add_to_journal(user_id="guest", beer_id=beer_id, user_rating=rating, user_notes=notes)
    st.success("Saved to your tasting journal! 🍻")
