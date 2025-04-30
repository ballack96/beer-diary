import streamlit as st
st.set_page_config(page_title="🗺️ Brewery Locator", layout="wide")

import pandas as pd
import requests
import plotly.express as px

# ------------------------------
# Theme Toggle (Light/Dark)
# ------------------------------
theme = st.sidebar.radio("🌓 Theme", ["Light", "Dark"], horizontal=True)
plotly_theme = "plotly_white" if theme == "Light" else "plotly_dark"

# ------------------------------
# Function to fetch breweries
# ------------------------------
@st.cache_data
def fetch_breweries():
    url = "https://api.openbrewerydb.org/v1/breweries?per_page=500"
    response = requests.get(url)
    if response.status_code == 200:
        breweries = response.json()
        df = pd.DataFrame(breweries)
        df = df[[
            "id", "name", "city", "state", "country",
            "latitude", "longitude", "website_url", "brewery_type"
        ]]
        df = df.dropna(subset=["latitude", "longitude"])
        df["latitude"] = df["latitude"].astype(float)
        df["longitude"] = df["longitude"].astype(float)
        return df
    else:
        st.error("❌ Failed to fetch brewery data.")
        return pd.DataFrame()

# ------------------------------
# Truncate Long Chip Labels
# ------------------------------
def truncate_label(label, max_len=22):
    return label if len(label) <= max_len else label[:max_len] + "..."

# ------------------------------
# Page Setup
# ------------------------------
st.title("🗺️ Brewery Locator")

if st.button("🔄 Refresh Breweries"):
    st.cache_data.clear()
    st.rerun()

breweries_df = fetch_breweries()

if breweries_df.empty:
    st.warning("No brewery data found.")
else:
    st.sidebar.header("🔎 Filter Breweries")

    # ------------------------------
    # Multiselect - State → City
    # ------------------------------
    all_states = sorted(breweries_df['state'].dropna().unique())
    state_labels = [truncate_label(state) for state in all_states]
    state_lookup = dict(zip(state_labels, all_states))

    selected_state_labels = st.sidebar.multiselect("Select State(s)", state_labels, default=state_labels)
    selected_states = [state_lookup[label] for label in selected_state_labels]

    state_filtered_df = breweries_df[breweries_df['state'].isin(selected_states)]

    all_cities = sorted(state_filtered_df['city'].dropna().unique())
    city_labels = [truncate_label(city) for city in all_cities]
    city_lookup = dict(zip(city_labels, all_cities))

    selected_city_labels = st.sidebar.multiselect("Select City(s)", city_labels, default=city_labels)
    selected_cities = [city_lookup[label] for label in selected_city_labels]

    all_types = sorted(breweries_df['brewery_type'].dropna().unique())
    selected_types = st.sidebar.multiselect("Select Brewery Type(s)", all_types, default=all_types)

    # ------------------------------
    # Apply Filters
    # ------------------------------
    filtered_df = breweries_df[
        (breweries_df['state'].isin(selected_states)) &
        (breweries_df['city'].isin(selected_cities)) &
        (breweries_df['brewery_type'].isin(selected_types))
    ]

    st.markdown(f"### 🔍 Showing {len(filtered_df)} breweries")

    # ------------------------------
    # Brewery Map
    # ------------------------------
    st.map(filtered_df[['latitude', 'longitude']])

    # ------------------------------
    # Brewery Type Breakdown
    # ------------------------------
    st.markdown("### 📊 Brewery Type Breakdown")

    type_counts = filtered_df['brewery_type'].value_counts().reset_index()
    type_counts.columns = ['type', 'count']

    fig1 = px.bar(
        type_counts,
        x='type',
        y='count',
        title='Distribution of Brewery Types',
        labels={'type': 'Type', 'count': 'Count'},
        template=plotly_theme,
        color='type'
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ------------------------------
    # Top Cities by Number of Breweries ✅ FIXED
    # ------------------------------
    st.markdown("### 🏙️ Top Cities by Number of Breweries")

    top_cities = (
        filtered_df['city']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'city', 'city': 'count'})
        .head(10)
    )

    fig2 = px.bar(
        top_cities,
        x='city',
        y='count',
        title='Top 10 Cities with Most Breweries (Filtered)',
        labels={'city': 'City', 'count': 'Brewery Count'},
        template=plotly_theme,
        color='count',
        color_continuous_scale='blues'
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ------------------------------
    # Brewery Table
    # ------------------------------
    st.markdown("### 🧾 Filtered Breweries Table")
    st.dataframe(
        filtered_df[['name', 'city', 'state', 'brewery_type', 'website_url']],
        use_container_width=True
    )

