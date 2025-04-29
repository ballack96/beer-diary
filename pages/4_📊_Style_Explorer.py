import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

def get_connection():
    return sqlite3.connect('craft_beer.db')

def load_beers():
    conn = get_connection()
    beers_df = pd.read_sql_query("SELECT * FROM beers", conn)
    conn.close()
    return beers_df

st.title("📊 Beer Style Explorer")

beers = load_beers()

fig = px.scatter(
    beers, 
    x="abv", 
    y="ibu", 
    color="style",
    hover_data=["name", "brewery_name"],
    labels={"abv": "Alcohol % (ABV)", "ibu": "Bitterness (IBU)"},
    title="ABV vs IBU by Beer Style"
)
st.plotly_chart(fig, use_container_width=True)
