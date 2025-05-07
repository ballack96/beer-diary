import streamlit as st
st.set_page_config(page_title="🗺️ Brewery Locator", page_icon="🗺️", layout="wide")

from theme_utils import get_app_theme
base, text_color, bg_color, card_color, plotly_template = get_app_theme()


import pydeck as pdk
import pandas as pd
import sqlite3
import requests
import plotly.express as px

# ------------------------------
# DB Connection & Add to Favorites
# ------------------------------
def get_connection():
    return sqlite3.connect('craft_beer.db')

def add_to_favorites(row, user_id="guest"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM favorite_breweries
        WHERE brewery_name = ? AND city = ? AND user_id = ?
    """, (row["name"], row["city"], user_id))

    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO favorite_breweries (brewery_name, city, state, country, website_url, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (row["name"], row["city"], row["state"], row["country"], row["website_url"], user_id))
        conn.commit()
        st.success(f"✅ Added {row['name']} to favorites.")
    else:
        st.info(f"ℹ️ {row['name']} is already in your favorites.")
    conn.close()

# ------------------------------
# API Fetch with Pagination
# ------------------------------
@st.cache_data
def fetch_breweries(page=1, per_page=100):
    url = f"https://api.openbrewerydb.org/v1/breweries?per_page={per_page}&page={page}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        breweries = response.json()
        if isinstance(breweries, list):
            df = pd.DataFrame(breweries)
            cols = ["id", "name", "city", "state", "country", "latitude", "longitude", "website_url", "brewery_type"]
            df = df[[col for col in cols if col in df.columns]]
            df = df.dropna(subset=["latitude", "longitude"])
            df["latitude"] = df["latitude"].astype(float)
            df["longitude"] = df["longitude"].astype(float)
            return df
        else:
            st.error("Unexpected format from OpenBreweryDB.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return pd.DataFrame()

# ------------------------------
# UI Start
# ------------------------------
st.markdown(f"<style>body {{ background-color: {bg_color}; color: {text_color}; }}</style>", unsafe_allow_html=True)
st.markdown(f"<h1>🗺️ Brewery Locator</h1>", unsafe_allow_html=True)

# Pagination Controls (inline)
col1, col2 = st.columns(2)
with col1:
    per_page = st.selectbox("🔢 Breweries per page", [25, 50, 100], index=1)
with col2:
    page_num = st.number_input("📄 Page #", min_value=1, value=1, step=1)

breweries_df = fetch_breweries(page=page_num, per_page=per_page)

if breweries_df.empty:
    st.warning("No brewery data found.")
    st.stop()

# ------------------------------
# Sidebar Filters
# ------------------------------
st.sidebar.header("🔎 Filter Breweries")
MAX_CHIPS = 12

# State Filter
all_states = sorted(breweries_df['state'].dropna().unique())
show_all_states = st.sidebar.checkbox("Show all states", value=False)
selected_states = st.sidebar.multiselect("Select State(s)", all_states, default=all_states if show_all_states else all_states[:MAX_CHIPS])

# City Filter (dependent on state)
filtered_by_state = breweries_df[breweries_df['state'].isin(selected_states)]
all_cities = sorted(filtered_by_state['city'].dropna().unique())
show_all_cities = st.sidebar.checkbox("Show all cities", value=False)
selected_cities = st.sidebar.multiselect("Select City(s)", all_cities, default=all_cities if show_all_cities else all_cities[:MAX_CHIPS])

# Brewery Type
all_types = sorted(breweries_df['brewery_type'].dropna().unique())
show_all_types = st.sidebar.checkbox("Show all brewery types", value=False)
selected_types = st.sidebar.multiselect("Select Brewery Type(s)", all_types, default=all_types if show_all_types else all_types[:MAX_CHIPS])

# Apply Filters
filtered_df = breweries_df[
    (breweries_df['state'].isin(selected_states)) &
    (breweries_df['city'].isin(selected_cities)) &
    (breweries_df['brewery_type'].isin(selected_types))
]

st.markdown(f"### 🔍 Showing {len(filtered_df)} breweries")

# ------------------------------
# Map
# ------------------------------
map_style = "mapbox://styles/mapbox/light-v10" if base == "light" else "mapbox://styles/mapbox/dark-v10"
st.pydeck_chart(pdk.Deck(
    map_style=map_style,
    initial_view_state=pdk.ViewState(latitude=39.5, longitude=-98.35, zoom=3),
    layers=[pdk.Layer(
        "ScatterplotLayer",
        data=filtered_df,
        get_position='[longitude, latitude]',
        get_color='[200, 30, 0, 160]',
        get_radius=40000,
    )],
))

# ------------------------------
# Charts
# ------------------------------
st.markdown("### 📊 Brewery Type Breakdown")
type_counts = filtered_df['brewery_type'].value_counts().reset_index()
type_counts.columns = ['type', 'count']
fig1 = px.bar(
    type_counts, x='type', y='count', title='Distribution of Brewery Types',
    template=plotly_template, color='type'
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("### 🏙️ Top Cities by Number of Breweries")
top_cities = filtered_df['city'].dropna().value_counts().reset_index().rename(columns={'index': 'city', 'city': 'count'}).head(10)
fig2 = px.bar(top_cities, x='city', y='count', title='Top Cities by Brewery Count', color='count', template=plotly_template)
st.plotly_chart(fig2, use_container_width=True)

# ------------------------------
# Paginated Table with Favorites
# ------------------------------
st.markdown("### 🧾 Filtered Breweries Table")
page_size = 10
total_pages = (len(filtered_df) - 1) // page_size + 1
table_page = st.number_input("Table Page", min_value=1, max_value=total_pages, value=1)
start_idx = (table_page - 1) * page_size
end_idx = start_idx + page_size

paged_df = filtered_df.iloc[start_idx:end_idx]
for i, row in paged_df.iterrows():
    cols = st.columns([3, 3, 2, 2, 1])
    cols[0].markdown(f"**{row['name']}**")
    cols[1].markdown(f"{row['city']}, {row['state']}")
    cols[2].markdown(f"[🌐 Website]({row['website_url']})" if row["website_url"] else "—")
    if cols[4].button("❤️ Favorite", key=f"fav_{row['id']}"):
        add_to_favorites(row)
