import streamlit as st
st.set_page_config(page_title="📊 Beer Style Explorer", page_icon="📈", layout="wide")

import sqlite3
import pandas as pd
import plotly.express as px

# ------------------------------
# Theme Toggle (Light/Dark)
# ------------------------------
theme = st.sidebar.radio("🌓 Theme", ["Light", "Dark"], horizontal=True)
plotly_theme = "plotly_white" if theme == "Light" else "plotly_dark"

# ------------------------------
# Database Connection
# ------------------------------
def get_connection():
    return sqlite3.connect('craft_beer.db')

# Load beers from the correct table
@st.cache_data
def load_beers():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM beers_catalog", conn)
    conn.close()
    return df

# ------------------------------
# Streamlit Page
# ------------------------------
st.title("📊 Beer Style Explorer")

# Load Data
beers_df = load_beers()

if beers_df.empty:
    st.warning("No beers found in the database.")
else:
    # -------------------------------
    # Sidebar Filters with Truncated Chips + Expand Toggle
    # -------------------------------
    st.sidebar.header("🔎 Filter Beers")
    MAX_CHIPS = 15  # Adjust based on space

    # --- Style Filter ---
    all_styles = sorted(beers_df['style'].dropna().unique())
    show_all_styles = st.sidebar.checkbox("Show all styles", value=False)
    default_styles = all_styles if show_all_styles else all_styles[:MAX_CHIPS]

    selected_styles = st.sidebar.multiselect(
        "Select Beer Style(s)", all_styles, default=default_styles
    )

    # --- ABV Range Filter ---
    abv_min = float(beers_df['abv'].min())
    abv_max = float(beers_df['abv'].max())
    selected_abv = st.sidebar.slider("ABV Range (%)", abv_min, abv_max, (abv_min, abv_max))

    # Filtering
    filtered_df = beers_df.copy()

    if selected_styles:
        filtered_df = filtered_df[filtered_df['style'].isin(selected_styles)]

    filtered_df = filtered_df[
        (filtered_df['abv'] >= selected_abv[0]) & (filtered_df['abv'] <= selected_abv[1])
    ]

    # Summary Metrics
    st.markdown("## 📋 Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Number of Beers", len(filtered_df))
    with col2:
        st.metric("Average ABV (%)", round(filtered_df['abv'].mean(), 2))
    with col3:
        st.metric("Average IBU", round(filtered_df['ibu'].mean(), 2))

    st.markdown("---")

    # 📊 Beer Style Distribution Toggle
    st.markdown("### 🍺 Beer Style Distribution")
    view_mode = st.radio("Choose Chart Type:", ["Bar Chart", "Pie Chart"], horizontal=True)

    style_counts = filtered_df['style'].value_counts().reset_index()
    style_counts.columns = ['style', 'count']

    if view_mode == "Bar Chart":
        fig = px.bar(
            style_counts,
            x='style',
            y='count',
            title='Beer Styles - Number of Beers',
            labels={'style': 'Beer Style', 'count': 'Number of Beers'},
            color='count',
            color_continuous_scale='viridis',
            template=plotly_theme
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.pie(
            style_counts,
            names='style',
            values='count',
            title='Beer Styles - Distribution (Pie Chart)',
            hole=0.4,
            template=plotly_theme
        )
        st.plotly_chart(fig, use_container_width=True)

    # 📊 ABV Distribution Histogram
    st.markdown("### 🍷 ABV Distribution")
    fig2 = px.histogram(
        filtered_df,
        x='abv',
        nbins=20,
        title='ABV (%) Distribution',
        labels={'abv': 'Alcohol By Volume (%)'},
        template=plotly_theme
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 🧪 Bubble Chart - Style vs Avg ABV + Breweries in tooltip
    st.markdown("### 🧪 Avg ABV by Style (Bubble Chart w/ Breweries)")

    # Create brewery samples per style
    brewery_samples = (
        filtered_df.groupby('style')['brewery_name']
        .apply(lambda x: ', '.join(x.dropna().unique()[:3]))
        .reset_index()
        .rename(columns={'brewery_name': 'example_breweries'})
    )

    bubble_df = (
        filtered_df.groupby('style')
        .agg(average_abv=('abv', 'mean'), count=('style', 'count'))
        .reset_index()
        .merge(brewery_samples, on='style', how='left')
    )

    fig3 = px.scatter(
        bubble_df,
        x='average_abv',
        y='count',
        size='count',
        color='style',
        hover_name='style',
        hover_data={'average_abv': True, 'count': True, 'example_breweries': True},
        title='Beer Styles: Avg ABV vs Frequency (with Brewery Examples)',
        labels={'average_abv': 'Avg ABV (%)', 'count': 'Number of Beers'},
        template=plotly_theme
    )
    st.plotly_chart(fig3, use_container_width=True)

    # 📋 Filtered Beer Table
    st.markdown("### 📚 Beers Matching Your Filters")
    st.dataframe(
        filtered_df[['beer_name', 'brewery_name', 'style', 'abv', 'ibu', 'description']],
        use_container_width=True
    )
