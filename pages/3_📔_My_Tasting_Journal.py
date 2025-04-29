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

# Function to get color badge based on average rating
def get_rating_badge(avg_rating):
    if avg_rating >= 4.0:
        color = "🟢 Excellent"
    elif avg_rating >= 3.0:
        color = "🟡 Good"
    elif avg_rating >= 2.0:
        color = "🟠 Average"
    else:
        color = "🔴 Poor"
    return color

# ------------------------------
# Streamlit Page
# ------------------------------
st.title("📔 My Tasting Journal")

journal_df = load_journal(user_id="guest")

if journal_df.empty:
    st.info("You haven't rated any beers yet! Go explore and add some. 🍻")
else:
    st.write(f"Total Beers Rated: **{len(journal_df)}**")

    # Export Button
    st.markdown("---")
    csv = journal_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download My Tasting Journal as CSV",
        data=csv,
        file_name='tasting_journal.csv',
        mime='text/csv'
    )

    # Display Journal Entries
    for idx, row in journal_df.iterrows():
        st.markdown("---")
        st.markdown(f"### 🍺 {row['beer_id']}")

        # Ratings Breakdown
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

        avg_rating = round(row['average_rating'], 2)
        badge = get_rating_badge(avg_rating)

        st.markdown(f"**Average Rating:** {avg_rating}/5 {badge}")
        st.markdown(f"**Notes:** {row['user_notes']}")
        st.caption(f"Tasted on: {row['tasted_on']}")
