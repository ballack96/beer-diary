import streamlit as st

st.set_page_config(page_title="🍻 Beer Diary", page_icon="🍺", layout="wide")

st.title("🍻 Welcome to Beer Diary!")

st.markdown("""
Track your beer tasting journey, explore craft beers,  
and save your personalized tasting notes!

**Pages Available:**
- 🍺 Explore Beers
- 📔 My Tasting Journal
- 🗺️ Brewery Locator

---
""")

st.image("https://images.unsplash.com/photo-1514516870926-206b6c1bb28d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDJ8fGJlZXJ8ZW58MHx8fHwxNjg2MzcxOTcz&ixlib=rb-4.0.3&q=80&w=1080", use_column_width=True)
