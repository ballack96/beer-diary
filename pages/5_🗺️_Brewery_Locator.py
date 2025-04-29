import streamlit as st
import pandas as pd
import requests
import sqlite3
import plotly.express as px


# ------------------------------
# Function to fetch breweries
# ------------------------------
@st.cache_data
def fetch_breweries():
    url = "https://api.openbrewerydb.org/v1/breweries?per_page=80"
    response = requests.get(url)
    if response.status_code == 200:
        breweries = response.json()
        df = pd.DataFrame(breweries)
        # Keep only useful columns
        df = df[["id", "name", "city", "state", "country", "latitude", "longitude", "website_url", "brewery_type"]]
        df = df.dropna(subset=["latitude", "longitude"])
        df["latitude"] = df["latitude"].astype(float)
        df["longitude"] = df["longitude"].astype(float)
        return df
    else:
        st.error("Failed to fetch brewery data.")
        return pd.DataFrame()

# ------------------------------
# Database connection
# ------------------------------
def get_connection():
    return sqlite3.connect('craft_beer.db')

# Save favorite brewery
def save_favorite_brewery(user_id, brewery):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if brewery already saved for this user
    cursor.execute('''
        SELECT * FROM favorite_breweries
        WHERE user_id = ? AND brewery_name = ?
    ''', (user_id, brewery['name']))
    existing = cursor.fetchone()

    if existing:
        st.info(f"🍺 {brewery['name']} is already in your favorites!")
    else:
        cursor.execute('''
            INSERT INTO favorite_breweries (user_id, brewery_name, city, state, country, website_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, brewery['name'], brewery['city'], brewery['state'], brewery['country'], brewery['website_url']))
        conn.commit()
        st.success(f"✅ Saved {brewery['name']} to your favorites! 🍻")

    conn.close()


# ------------------------------
# Streamlit page
# ------------------------------
st.title("🗺️ Brewery Map Locator (Live)")

if st.button("🔄 Refresh Breweries"):
    st.cache_data.clear()
    st.rerun()

breweries_df = fetch_breweries()

if breweries_df.empty:
    st.warning("No breweries found. Please try refreshing.")
else:
    # Sidebar Filters
    st.sidebar.header("🔎 Filter Breweries")

    # Multi-select for State
    all_states = sorted(breweries_df['state'].dropna().unique())
    selected_states = st.sidebar.multiselect("Select State(s)", all_states, default=all_states)

    # Filter by selected states
    filtered_df = breweries_df[breweries_df['state'].isin(selected_states)]

    # Multi-select for City (only cities in selected states)
    all_cities = sorted(filtered_df['city'].dropna().unique())
    selected_cities = st.sidebar.multiselect("Select City(s)", all_cities, default=all_cities)

    # Final filtered DataFrame
    filtered_df = filtered_df[filtered_df['city'].isin(selected_cities)]

    # Multi-select for Brewery Type
    all_types = sorted(filtered_df['brewery_type'].dropna().unique())
    selected_types = st.sidebar.multiselect("Select Brewery Type(s)", all_types, default=all_types)

    # Filter by selected types
    filtered_df = filtered_df[filtered_df['brewery_type'].isin(selected_types)]

    states = sorted(breweries_df['state'].dropna().unique())
    selected_state = st.sidebar.selectbox("Select State", ["All"] + states)

    filtered_df = breweries_df.copy()
    if selected_state != "All":
        filtered_df = filtered_df[filtered_df['state'] == selected_state]

        cities = sorted(filtered_df['city'].dropna().unique())
        selected_city = st.sidebar.selectbox("Select City", ["All"] + cities)

        if selected_city != "All":
            filtered_df = filtered_df[filtered_df['city'] == selected_city]

    # Map
    st.subheader(f"Showing {len(filtered_df)} Breweries")
    st.map(filtered_df[['latitude', 'longitude']])

    # Brewery Selector
    st.subheader("🏭 Select a Brewery")
    selected_brewery = st.selectbox(
        "Choose a brewery to see details",
        options=filtered_df['name'].tolist()
    )

    # Display Pretty Brewery Card
    if selected_brewery:
        brewery_details = filtered_df[filtered_df['name'] == selected_brewery].iloc[0]

        st.markdown("---")
        col1, col2 = st.columns([1, 2])

        with col1:
            # Placeholder brewery image (You can update this to actual brewery logos later)
            st.image("https://cdn-icons-png.flaticon.com/512/2329/2329163.png", width=150)

        with col2:
            st.markdown(f"### 🍺 {brewery_details['name']}")
            st.markdown(f"**Type:** {brewery_details['brewery_type'].capitalize()}")
            st.markdown(f"**Location:** {brewery_details['city']}, {brewery_details['state']}, {brewery_details['country']}")
            if brewery_details['website_url']:
                st.markdown(f"**Website:** [Visit Website]({brewery_details['website_url']})")

            # Save to Favorites Button
            if st.button("💾 Save to Favorites"):
                save_favorite_brewery(user_id="guest", brewery=brewery_details)
                st.success(f"Saved {brewery_details['name']} to your favorites! 🍻")

        # Mini map for the selected brewery
        st.map(pd.DataFrame({
            'latitude': [brewery_details['latitude']],
            'longitude': [brewery_details['longitude']]
        }))


    # Brewery Type Breakdown
    if not filtered_df.empty:
        st.markdown("### 📊 Brewery Type Breakdown")
        brewery_counts = filtered_df['brewery_type'].value_counts().reset_index()
        brewery_counts.columns = ['brewery_type', 'count']

        fig = px.bar(
            brewery_counts,
            x='brewery_type',
            y='count',
            color='brewery_type',
            title='Distribution of Brewery Types (Filtered)',
            labels={'brewery_type': 'Type', 'count': 'Count'},
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Top Cities by Brewery Count
    if not filtered_df.empty:
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
            template='plotly_white',
            color='count',
            color_continuous_scale='blues'
        )
        st.plotly_chart(fig2, use_container_width=True)
