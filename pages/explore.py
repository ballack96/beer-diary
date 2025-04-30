import streamlit as st
st.set_page_config(page_title="🍻 Explore Beers", page_icon="🍺", layout="wide")

import sqlite3
import pandas as pd
import datetime

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
st.title("🍻 Explore Beers (Database Loaded)")

# -------------------------------
# Initialize Journal in Session
# -------------------------------
if "journal" not in st.session_state:
    st.session_state["journal"] = []

# -------------------------------
# Load Beers
# -------------------------------
beers_df = load_beers()

if beers_df.empty:
    st.warning("No beers found in the database.")
else:
    # -------------------------------
    # Sidebar Filters with Truncated Chips + Expand Toggle
    # -------------------------------
    st.sidebar.header("🔎 Filter Beers")
    MAX_CHIPS = 15  # Limit initial visible chips

    # --- Style Filter ---
    all_styles = sorted(beers_df['style'].dropna().unique())
    show_all_styles = st.sidebar.checkbox("Show all styles", value=False)
    default_styles = all_styles if show_all_styles else all_styles[:MAX_CHIPS]

    selected_styles = st.sidebar.multiselect(
        "Select Beer Style(s)",
        options=all_styles,
        default=default_styles
    )

    # --- ABV Range Filter ---
    abv_min = float(beers_df['abv'].min())
    abv_max = float(beers_df['abv'].max())
    selected_abv = st.sidebar.slider("Select ABV Range (%)", abv_min, abv_max, (abv_min, abv_max))

    # --- Optional Name Search ---
    search_term = st.text_input("🔍 Search beer name...")

    # -------------------------------
    # Apply Filter Logic
    # -------------------------------
    filtered_df = beers_df.copy()

    if selected_styles:
        filtered_df = filtered_df[filtered_df['style'].isin(selected_styles)]

    filtered_df = filtered_df[
        (filtered_df['abv'] >= selected_abv[0]) & (filtered_df['abv'] <= selected_abv[1])
    ]

    if search_term:
        filtered_df = filtered_df[filtered_df['beer_name'].str.contains(search_term, case=False)]

    st.markdown(f"### Showing {len(filtered_df)} matching beers")

    for _, row in filtered_df.iterrows():
        beer_id = row['beer_name']  # unique ID

        with st.container():
            st.subheader(f"🍺 {row['beer_name']}")
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
                        st.success(f"✅ '{beer_id}' saved to your tasting journal!")
                    else:
                        st.info(f"'{beer_id}' is already in your journal.")