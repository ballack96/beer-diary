import streamlit as st
st.set_page_config(page_title="📊 Beer Style Explorer", page_icon="📈", layout="wide")


from theme_utils import get_app_theme
base, text_color, bg_color, card_color, plotly_template = get_app_theme()



import sqlite3
import pandas as pd
import plotly.express as px

# ------------------------------
# DB Connection
# ------------------------------
def get_connection():
    return sqlite3.connect("craft_beer.db")

@st.cache_data
def load_beers():
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM beers_catalog", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
        return pd.DataFrame()

# ------------------------------
# Header
# ------------------------------
st.markdown(f"<style>body {{ background-color: {bg_color}; color: {text_color}; }}</style>", unsafe_allow_html=True)
st.markdown(f"<h1>📊 Style Explorer</h1>", unsafe_allow_html=True)

beers_df = load_beers()
if beers_df.empty:
    st.warning("No beers found in the database.")
    st.stop()

# -------------------------------
# Sidebar Filters
# -------------------------------
with st.sidebar.expander("🎛️ Filters", expanded=True):
    MAX_CHIPS = 15
    all_styles = sorted(beers_df["style"].dropna().unique())
    show_all_styles = st.checkbox("Show all styles", value=False)
    default_styles = all_styles if show_all_styles else all_styles[:MAX_CHIPS]
    selected_styles = st.multiselect("Select Beer Style(s)", options=all_styles, default=default_styles)

    abv_min = float(beers_df["abv"].min())
    abv_max = float(beers_df["abv"].max())
    selected_abv = st.slider("ABV Range", abv_min, abv_max, (abv_min, abv_max))

# -------------------------------
# Apply Filter Logic
# -------------------------------
filtered_df = beers_df.copy()

if selected_styles:
    filtered_df = filtered_df[filtered_df["style"].isin(selected_styles)]

filtered_df = filtered_df[
    (filtered_df["abv"] >= selected_abv[0]) & (filtered_df["abv"] <= selected_abv[1])
]

if filtered_df.empty:
    st.warning("No matching beers. Try relaxing your filters.")
    st.stop()

# -------------------------------
# Summary Metrics
# -------------------------------
st.markdown("## 📋 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Number of Beers", len(filtered_df))
col2.metric("Average ABV (%)", round(filtered_df["abv"].mean(), 2))
col3.metric("Average IBU", round(filtered_df["ibu"].mean(), 2))

st.markdown("---")

# -------------------------------
# Style Distribution Chart
# -------------------------------
st.markdown("### 🍺 Beer Style Distribution")
view_mode = st.radio("Choose Chart Type:", ["Bar Chart", "Pie Chart"], horizontal=True)

style_counts = filtered_df["style"].value_counts().reset_index()
style_counts.columns = ["style", "count"]

if view_mode == "Bar Chart":
    fig = px.bar(
        style_counts,
        x="style",
        y="count",
        title="Beer Styles - Number of Beers",
        labels={"style": "Beer Style", "count": "Count"},
        color="count",
        color_continuous_scale="viridis",
        template=plotly_template
    )
else:
    fig = px.pie(
        style_counts,
        names="style",
        values="count",
        title="Beer Styles - Distribution",
        hole=0.4,
        template=plotly_template
    )

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# ABV Histogram
# -------------------------------
st.markdown("### 🍷 ABV Distribution")
fig2 = px.histogram(
    filtered_df,
    x="abv",
    nbins=20,
    title="ABV (%) Distribution",
    labels={"abv": "Alcohol By Volume (%)"},
    template=plotly_template
)
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# Bubble Chart: Avg ABV vs Count
# -------------------------------
st.markdown("### 🧪 Avg ABV by Style (Bubble Chart w/ Breweries)")

brewery_samples = (
    filtered_df.groupby("style")["brewery_name"]
    .apply(lambda x: ", ".join(x.dropna().unique()[:3]))
    .reset_index()
    .rename(columns={"brewery_name": "example_breweries"})
)

bubble_df = (
    filtered_df.groupby("style")
    .agg(average_abv=("abv", "mean"), count=("style", "count"))
    .reset_index()
    .merge(brewery_samples, on="style", how="left")
)

fig3 = px.scatter(
    bubble_df,
    x="average_abv",
    y="count",
    size="count",
    color="style",
    hover_name="style",
    hover_data={"average_abv": True, "count": True, "example_breweries": True},
    title="Beer Styles: Avg ABV vs Frequency (with Brewery Examples)",
    labels={"average_abv": "Avg ABV (%)", "count": "Beers"},
    template=plotly_template
)
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# Filtered Table
# -------------------------------
st.markdown("### 📚 Matching Beers")
st.dataframe(
    filtered_df[["beer_name", "brewery_name", "style", "abv", "ibu", "description"]],
    use_container_width=True
)