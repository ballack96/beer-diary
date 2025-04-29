import streamlit as st
import sqlite3
import pandas as pd

# Database connection
def get_connection():
    return sqlite3.connect('craft_beer.db')

# Load tasting journal entries
@st.cache_data
def load_journal(user_id):
    conn = get_connection()
    df = pd.read_sql_query(f'''
        SELECT journal_id, beer_id, look, smell, taste, feel, overall, average_rating, user_notes, tasted_on
        FROM tasting_journal
        WHERE user_id = '{user_id}'
        ORDER BY tasted_on DESC
    ''', conn)
    conn.close()
    return df

# ------------------------------
# Streamlit Page
# ------------------------------
st.title("📔 My Tasting Journal")

journal_df = load_journal(user_id="guest")

if journal_df.empty:
    st.info("You haven't rated any beers yet! Go explore and add some. 🍻")
else:
    st.write(f"Total Beers Rated: **{len(journal_df)}**")

    for idx, row in journal_df.iterrows():
        st.markdown("---")
        st.markdown(f"### 🍺 {row['beer_id']}")

        # Ratings Breakdown in columns
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("👀 Look", f"{row['look']}/5")
        with col2:
            st.metric("👃 Smell", f"{row['smell']}/5")
        with col3:
            st.metric("👅 Taste", f"{row['taste']}/5")
        with col4:
            st.metric("🖐️ Feel", f"{row['feel']}/5")
        with col5:
            st.metric("⭐ Overall", f"{row['overall']}/5")

        st.markdown(f"**Average Rating:** {round(row['average_rating'],2)}/5 ⭐")

        # Notes and Tasting Date
        st.markdown(f"**Notes:** {row['user_notes']}")
        st.caption(f"Tasted on: {row['tasted_on']}")
