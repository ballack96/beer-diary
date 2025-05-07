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
st.markdown(f"<p>Track your beer tasting journey, explore craft beers, and save your notes.</p>", unsafe_allow_html=True)

# # Load and show images from static/images folder
# image_folder = os.path.join("static", "images")
# image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith((".png", ".jpg", ".jpeg"))]
# image_files.sort()  # Optional, ensures ordered display

# # Show images in 2x2 grid
# cols = st.columns(2)
# for idx, img_path in enumerate(image_files[:4]):  # Show only first 4
#     with cols[idx % 2]:
#         with open(img_path, "rb") as f:
#             st.image(f.read(), use_column_width=True)


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