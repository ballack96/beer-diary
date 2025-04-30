import streamlit as st
st.set_page_config(page_title="🍻 Beer Diary", page_icon="🍺", layout="wide")

import os
from init_db import initialize_database_if_needed

initialize_database_if_needed()


theme = st.sidebar.radio("🌓 Theme", ["Light", "Dark"], horizontal=True)

st.title("🍻 Welcome to Beer Diary")

st.markdown("""
Track your beer tasting journey, explore craft beers, and save your tasting notes.

#### Pages:
- 🍺 Explore Beers
- 🧾 My Tasting Journal
- 📊 Style Explorer
- 🗺️ Brewery Locator
- 📜 My Favorite Breweries
""")

st.image("https://images.unsplash.com/photo-1514516870926-206b6c1bb28d", use_column_width=True)