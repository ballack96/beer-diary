import streamlit as st
st.set_page_config(page_title="📜 My Favorite Breweries", page_icon="📈", layout="wide")
# Import theme utilities
try:
    from theme_utils import apply_theme
    # Apply the theme and get the current theme name
    current_theme = apply_theme()
except ImportError:
    # Fallback if theme_utils.py doesn't exist yet
    if 'theme' not in st.session_state:
        st.session_state.theme = "Light"
    current_theme = st.sidebar.radio("🌓 Theme", ["Light", "Dark"], 
                            horizontal=True, 
                            index=0 if st.session_state.theme == "Light" else 1)
    if current_theme != st.session_state.theme:
        st.session_state.theme = current_theme

import sqlite3
import pandas as pd

# ------------------------------
# Database connection
# ------------------------------
def get_connection():
    return sqlite3.connect('craft_beer.db')

# Fetch favorite breweries
def load_favorites(user_id):
    conn = get_connection()
    favorites = pd.read_sql_query(f"""
        SELECT fav_id, brewery_name, city, state, country, website_url
        FROM favorite_breweries
        WHERE user_id = '{user_id}'
    """, conn)
    conn.close()
    return favorites

# Remove a favorite brewery
def remove_favorite(fav_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM favorite_breweries WHERE fav_id = ?', (fav_id,))
    conn.commit()
    conn.close()

# ------------------------------
# Streamlit Page
# ------------------------------
st.title("📜 My Favorite Breweries")

favorites_df = load_favorites(user_id="guest")

if favorites_df.empty:
    st.info("You haven't saved any favorite breweries yet! 🍻")
else:
    # Search bar
    search_term = st.text_input("🔍 Search Favorites by Brewery Name...")

    if search_term:
        favorites_df = favorites_df[favorites_df['brewery_name'].str.contains(search_term, case=False)]

    st.write(f"Showing {len(favorites_df)} favorite breweries:")

    for index, row in favorites_df.iterrows():
        st.markdown("---")
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"### 🍺 {row['brewery_name']}")
            st.markdown(f"**Location:** {row['city']}, {row['state']}, {row['country']}")
            if row['website_url']:
                st.markdown(f"**Website:** [Visit Website]({row['website_url']})")

        with col2:
            if st.button(f"🗑️ Remove", key=f"remove_{row['fav_id']}"):
                remove_favorite(row['fav_id'])
                st.success(f"Removed {row['brewery_name']} from favorites!")
                st.experimental_rerun()

    # Allow user to download favorites
    st.markdown("---")
    csv = favorites_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Favorites as CSV",
        data=csv,
        file_name='favorite_breweries.csv',
        mime='text/csv'
    )
