import streamlit as st
from init_db import initialize_database_if_needed
from theme_utils import get_app_theme

#  Only ONE call to set_page_config
st.set_page_config(
    page_title="🏠 Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme-aware colors
_, text_color, _, _, _ = get_app_theme()

st.markdown(f"<h1 style='color:{text_color}'>🏠 Welcome to Beer Diary</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:{text_color}'>Track your beer tasting journey, explore craft beers, and save notes.</p>", unsafe_allow_html=True)

# DB
initialize_database_if_needed()

st.markdown(f"""
### Pages:
- 🍺 **Explore Beers**
- 📓 **My Tasting Journal**
- 📊 **Style Explorer**
- 🗺️ **Brewery Locator**
- 📜 **My Favorite Breweries**
""", unsafe_allow_html=True)

st.image("https://images.unsplash.com/photo-1514516870926-206b6c1bb28d", use_column_width=True)

st.sidebar.markdown("### 🧭 Navigation")
st.sidebar.info("Use the pages dropdown in the sidebar to navigate.")
