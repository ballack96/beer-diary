import streamlit as st
import sqlite3
import pandas as pd

def get_connection():
    return sqlite3.connect('craft_beer.db')

st.title("📔 My Tasting Journal")

conn = get_connection()
journal = pd.read_sql_query("""
    SELECT tj.user_rating, tj.user_notes, b.name, b.style, b.abv
    FROM tasting_journal tj
    JOIN beers b ON tj.beer_id = b.beer_id
    WHERE tj.user_id = 'guest'
""", conn)
conn.close()

if not journal.empty:
    st.dataframe(journal)
else:
    st.info("No tasting entries yet. Go explore and add some beers! 🍻")
