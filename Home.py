import streamlit as st
# Must come first
st.set_page_config(page_title="🏠 Beer Diary", page_icon="🍺", layout="wide")

from theme_utils import get_app_theme


from PIL import Image
from pathlib import Path
import os

# Apply theme
base, text_color, bg_color, card_color, plotly_template = get_app_theme()

st.markdown(f"<style>body {{ background-color: {bg_color}; color: {text_color}; }}</style>", unsafe_allow_html=True)


# UI content
st.markdown(f"<h1>🏠 Welcome to Beer Diary</h1>", unsafe_allow_html=True)
st.markdown(f"<p>Welcome to your personalized craft beer tasting journal! Use the navigation panel to explore beers, styles, breweries, and keep track of your tasting notes. This app is designed to make your craft beer discovery more enjoyable, organized, and fun.</p>", unsafe_allow_html=True)

# Load and show images from static/images folder
image_folder = os.path.join("static", "images")
image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith((".png", ".jpg", ".jpeg"))]
image_files.sort()  # Optional, ensures ordered display

# Show images in 2x2 grid
cols = st.columns(len(image_files))
for i, path in enumerate(image_files):
    with open(path, "rb") as img_file:
        image = Image.open(img_file)
        cols[i].image(image, width=250)  # Smaller fixed width


st.markdown(f"""
### Pages:
- 🍺 Explore Beers
- 📓 My Tasting Journal
- 📊 Style Explorer
- 🗺️ Brewery Locator
- 📜 My Favorite Breweries
""", unsafe_allow_html=True)

# Instructions
st.sidebar.markdown("### 🧭 Navigation")
st.sidebar.info("Use the sidebar to explore beers, log tastings, and find breweries.")