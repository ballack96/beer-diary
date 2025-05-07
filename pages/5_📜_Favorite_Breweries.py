import streamlit as st
st.set_page_config(page_title="📜 My Favorite Breweries", page_icon="📜", layout="wide")

from theme_utils import get_app_theme
base, text_color, bg_color, card_color, plotly_template = get_app_theme()


import sqlite3
import pandas as pd

# ------------------------------
# DB Access Functions
# ------------------------------
def get_connection():
    return sqlite3.connect('craft_beer.db')

def load_favorites(user_id="guest"):
    conn = get_connection()
    favorites = pd.read_sql_query("""
        SELECT fav_id, brewery_name, city, state, country, website_url
        FROM favorite_breweries
        WHERE user_id = ?
    """, conn, params=(user_id,))
    conn.close()
    return favorites

def remove_favorite(fav_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM favorite_breweries WHERE fav_id = ?', (fav_id,))
    conn.commit()
    conn.close()

# ------------------------------
# Page Layout
# ------------------------------
st.markdown(f"<style>body {{ background-color: {bg_color}; color: {text_color}; }}</style>", unsafe_allow_html=True)
st.markdown(f"<h1>📜 My Favorite Breweries</h1>", unsafe_allow_html=True)
st.markdown(f"<p>Saved breweries you’ve added from the map view.</p>", unsafe_allow_html=True)

favorites_df = load_favorites(user_id="guest")

if favorites_df.empty:
    st.info("You haven't saved any favorite breweries yet! 🍻")
    st.stop()

# ------------------------------
# Search + Filter
# ------------------------------
search_term = st.text_input("🔍 Search by Brewery Name...")

if search_term:
    favorites_df = favorites_df[favorites_df['brewery_name'].str.contains(search_term, case=False)]

st.markdown(f"### Showing {len(favorites_df)} favorites")

# ------------------------------
# Paginated Brewery Cards
# ------------------------------
page_size = 5
total_pages = (len(favorites_df) - 1) // page_size + 1
page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
start = (page - 1) * page_size
end = start + page_size

paged_df = favorites_df.iloc[start:end]

for _, row in paged_df.iterrows():
    st.markdown("---")
    col1, col2 = st.columns([4, 1])

    with col1:
        st.subheader(f"🍺 {row['brewery_name']}")
        st.markdown(f"**Location:** {row['city']}, {row['state']}, {row['country']}")
        if row["website_url"]:
            st.markdown(f"[🌐 Website]({row['website_url']})", unsafe_allow_html=True)

    with col2:
        if st.button("🗑️ Remove", key=f"remove_{row['fav_id']}"):
            remove_favorite(row['fav_id'])
            st.success(f"Removed {row['brewery_name']} from favorites.")
            st.experimental_rerun()

# ------------------------------
# CSV Download
# ------------------------------
st.markdown("---")
csv = favorites_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Favorites CSV",
    data=csv,
    file_name='favorite_breweries.csv',
    mime='text/csv'
)