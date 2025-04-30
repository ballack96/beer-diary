import streamlit as st
import sqlite3
import pandas as pd

# -------------------------------
# Theme Toggle
# -------------------------------
theme = st.sidebar.radio("🌓 Theme", ["Light", "Dark"], horizontal=True)

# ------------------------------
# Database connection
# ------------------------------
def get_connection():
    return sqlite3.connect('craft_beer.db')

# Load beers from database
@st.cache_data(show_spinner=False)
def load_beers():
    conn = get_connection()
    df = pd.read_sql_query('SELECT * FROM beers_catalog', conn)
    conn.close()
    return df

# Save tasting journal with composite rating
def add_to_journal(user_id, beer_name, look, smell, taste, feel, overall, notes):
    conn = get_connection()
    cursor = conn.cursor()

    avg_rating = (look + smell + taste + feel + overall) / 5

    beer_id = beer_name

    cursor.execute('''
        INSERT INTO tasting_journal (user_id, beer_id, look, smell, taste, feel, overall, average_rating, user_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, beer_id, look, smell, taste, feel, overall, avg_rating, notes))
    conn.commit()
    conn.close()

# -------------------------------
# Truncate Labels for Chips (Optional)
# -------------------------------
def truncate_label(label, max_len=24):
    return label if len(label) <= max_len else label[:max_len] + "..."

# ------------------------------
# Streamlit Page
# ------------------------------
st.set_page_config(page_title="🍻 Explore Beers", page_icon="🍺", layout="wide")
st.title("🍻 Explore Beers (Database Loaded)")

# -------------------------------
# Load Data
# -------------------------------
beers_df = load_beers()

if beers_df.empty:
    st.warning("No beers found in database.")
else:
    st.sidebar.header("🔍 Filters")

    # -------------------------------
    # Filters
    # -------------------------------
    styles = sorted(beers_df['style'].dropna().unique())
    style_labels = [truncate_label(s) for s in styles]
    style_map = dict(zip(style_labels, styles))

    selected_style_labels = st.sidebar.multiselect("Select Beer Style(s)", style_labels, default=style_labels)
    selected_styles = [style_map[s] for s in selected_style_labels]

    abv_min = float(beers_df['abv'].min())
    abv_max = float(beers_df['abv'].max())
    selected_abv = st.sidebar.slider("Select ABV Range (%)", abv_min, abv_max, (abv_min, abv_max))

    search_term = st.text_input("🔍 Search for a beer by name...")

    # -------------------------------
    # Apply Filters
    # -------------------------------
    filtered_df = beers_df[
        (beers_df['style'].isin(selected_styles)) &
        (beers_df['abv'] >= selected_abv[0]) &
        (beers_df['abv'] <= selected_abv[1])
    ]

    if search_term:
        filtered_df = filtered_df[filtered_df['beer_name'].str.contains(search_term, case=False)]

    st.markdown(f"Showing {len(filtered_df)} beers:")

    # -------------------------------
    # Beer Cards
    # -------------------------------
    for _, row in filtered_df.iterrows():
        with st.container():
            st.subheader(f"🍺 {row['beer_name']}")
            st.markdown(f"**Brewery:** {row['brewery_name']}")
            st.markdown(f"**Style:** {row['style']}")
            st.markdown(f"**ABV:** {row['abv']}% | **IBU:** {row['ibu']}")
            st.markdown(f"**Description:** {row['description']}")
            with st.expander("➕ Add to Tasting Journal"):
                st.write("Tasting note/rating UI can go here.")