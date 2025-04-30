import streamlit as st
import os
from init_db import initialize_database_if_needed

# Set up page config first - before any other Streamlit commands
st.set_page_config(
    page_title="🍻 Beer Diary", 
    page_icon="🍺", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import theme utilities
# If this import fails, make sure to create theme_utils.py first
try:
    from theme_utils import apply_theme
    # Apply the theme
    theme = apply_theme()
except ImportError:
    # Fallback if theme_utils.py doesn't exist yet
    if 'theme' not in st.session_state:
        st.session_state.theme = "Light"
    theme = st.sidebar.radio("🌓 Theme", ["Light", "Dark"], 
                            horizontal=True, 
                            index=0 if st.session_state.theme == "Light" else 1)
    if theme != st.session_state.theme:
        st.session_state.theme = theme

# Initialize database
initialize_database_if_needed()

st.title("🍻 Welcome to Beer Diary")

st.markdown("""
Track your beer tasting journey, explore craft beers, and save your tasting notes.

#### Pages:
- 🍺 **Explore Beers** - Browse and search through our beer catalog
- 📓 **My Tasting Journal** - Keep track of your beer tasting experiences
- 📊 **Style Explorer** - Learn about different beer styles
- 🗺️ **Brewery Locator** - Find breweries near you
- 📜 **My Favorite Breweries** - Manage your list of favorite breweries
""")

st.image("https://images.unsplash.com/photo-1514516870926-206b6c1bb28d", use_column_width=True)

# Add instructions for navigation
st.sidebar.markdown("### 🧭 Navigation")
st.sidebar.info("Use the pages dropdown in the sidebar to navigate between different sections of the app.")