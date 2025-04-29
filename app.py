import streamlit as st
import pandas as pd

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
