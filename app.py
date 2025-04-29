import streamlit as st
import pandas as pd

import os
from init_db import initialize_database_if_needed

# Check if DB exists, if not, initialize
if not os.path.exists('craft_beer.db'):
    initialize_database_if_needed()

st.set_page_config(page_title="🍻 Craft Beer Dashboard", layout="wide")

with st.sidebar:
    st.markdown("## 🍺 Craft Beer Dashboard")
    st.markdown("---")

# Main page content
st.title("🍺 Craft Beer Enthusiasts Dashboard")
st.write("Use the sidebar to navigate between pages.")

st.markdown("""
---
**Pages Available**:
- Explore craft beers
- Track your tasting notes
- Explore beer styles with charts
""")
