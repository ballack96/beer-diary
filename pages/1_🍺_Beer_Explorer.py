import streamlit as st
st.set_page_config(page_title="🍻 Explore Beers", page_icon="🍺", layout="wide")

from theme_utils import get_app_theme
base, text_color, bg_color, card_color, plotly_template = get_app_theme()


import sqlite3
import pandas as pd
import datetime
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path

# ------------------------------
# Fallback Image Loader
# ------------------------------
def load_image_safe(url, fallback_filename="placeholder-1.png"):
    fallback_path = Path("static/images") / fallback_filename
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception:
        return Image.open(fallback_path)

# ------------------------------
# Database connection
# ------------------------------
def get_connection():
    return sqlite3.connect('craft_beer.db')

@st.cache_data(show_spinner=False)
def load_beers():
    try:
        conn = get_connection()
        df = pd.read_sql_query('SELECT * FROM beers_catalog', conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"⚠️ Failed to load beers: {e}")
        return pd.DataFrame()

# ------------------------------
# Save to Tasting Journal
# ------------------------------
def add_to_journal(user_id, beer_name, look, smell, taste, feel, overall, notes):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        avg_rating = (look + smell + taste + feel + overall) / 5
        cursor.execute('''
            INSERT INTO tasting_journal (user_id, beer_id, look, smell, taste, feel, overall, average_rating, user_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, beer_name, look, smell, taste, feel, overall, avg_rating, notes))
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"❌ Failed to save journal entry: {e}")

# -------------------------------
# Streamlit Page
# -------------------------------
st.markdown(f"<style>body {{ background-color: {bg_color}; color: {text_color}; }}</style>", unsafe_allow_html=True)
st.markdown(f"<h1>🍻 Explore Beers</h1>", unsafe_allow_html=True)

if "journal" not in st.session_state:
    st.session_state["journal"] = []

beers_df = load_beers()
if beers_df.empty:
    st.warning("🚫 No beers found in the database.")
    st.stop()

# -------------------------------
# Sidebar Filters
# -------------------------------
with st.sidebar.expander("🎛️ Filter Beers", expanded=True):
    MAX_CHIPS = 15
    all_styles = sorted(beers_df['style'].dropna().unique())
    show_all_styles = st.checkbox("Show all styles", value=False)
    default_styles = all_styles if show_all_styles else all_styles[:MAX_CHIPS]
    selected_styles = st.multiselect("Select Beer Style(s)", options=all_styles, default=default_styles)

    abv_min = float(beers_df['abv'].min())
    abv_max = float(beers_df['abv'].max())
    selected_abv = st.slider("Select ABV Range (%)", abv_min, abv_max, (abv_min, abv_max))

    search_term = st.text_input("🔍 Search beer name...")

# -------------------------------
# Apply Filters
# -------------------------------
filtered_df = beers_df.copy()

if selected_styles:
    filtered_df = filtered_df[filtered_df['style'].isin(selected_styles)]

filtered_df = filtered_df[
    (filtered_df['abv'] >= selected_abv[0]) & (filtered_df['abv'] <= selected_abv[1])
]

if search_term:
    filtered_df = filtered_df[filtered_df['beer_name'].str.contains(search_term, case=False)]

if filtered_df.empty:
    st.warning("🚫 No beers match your criteria. Try adjusting the filters.")
    st.stop()

# -------------------------------
# Display Beers
# -------------------------------
st.markdown(f"### Showing {len(filtered_df)} matching beers")

for _, row in filtered_df.iterrows():
    beer_id = row['beer_name']

    with st.container():
        st.subheader(f"🍺 {row['beer_name']}")
        # st.image(load_image_safe(row.get("image_url", "")), use_column_width=True)
        st.markdown(f"**Brewery:** {row['brewery_name']}")
        st.markdown(f"**Style:** {row['style']}")
        st.markdown(f"**ABV:** {row['abv']}% | **IBU:** {row['ibu']}")
        st.markdown(f"**Description:** {row['description']}")

        with st.expander("➕ Add to Tasting Journal"):
            col1, col2, col3, col4, col5 = st.columns(5)
            look = col1.slider("👀 Look", 0.0, 5.0, 2.5, 0.5, key=f"{beer_id}_look")
            smell = col2.slider("👃 Smell", 0.0, 5.0, 2.5, 0.5, key=f"{beer_id}_smell")
            taste = col3.slider("👅 Taste", 0.0, 5.0, 2.5, 0.5, key=f"{beer_id}_taste")
            feel = col4.slider("🖐️ Feel", 0.0, 5.0, 2.5, 0.5, key=f"{beer_id}_feel")
            overall = col5.slider("⭐ Overall", 0.0, 5.0, 2.5, 0.5, key=f"{beer_id}_overall")
            notes = st.text_area("📝 Notes", key=f"{beer_id}_notes")

            if st.button("💾 Save to Journal", key=f"{beer_id}_save"):
                if beer_id not in [j["beer_id"] for j in st.session_state["journal"]]:
                    st.session_state["journal"].append({
                        "beer_id": beer_id,
                        "brewery_name": row["brewery_name"],
                        "style": row["style"],
                        "abv": row["abv"],
                        "look": look,
                        "smell": smell,
                        "taste": taste,
                        "feel": feel,
                        "overall": overall,
                        "average_rating": round((look + smell + taste + feel + overall) / 5, 2),
                        "user_notes": notes,
                        "tasted_on": datetime.date.today().isoformat()
                    })
                    add_to_journal("guest", beer_id, look, smell, taste, feel, overall, notes)
                    st.success(f"✅ '{beer_id}' saved to your tasting journal!")
                else:
                    st.info(f"ℹ️ '{beer_id}' is already in your journal.")