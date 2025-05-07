import streamlit as st
st.set_page_config(page_title="📔 My Tasting Journal", page_icon="📔", layout="wide")


from theme_utils import get_app_theme
base, text_color, bg_color, card_color, plotly_template = get_app_theme()


import sqlite3
import pandas as pd

# -------------------------------
# DB Connection + Loader
# -------------------------------
def get_connection():
    return sqlite3.connect('craft_beer.db')

def load_journal_from_db(user_id="guest"):
    try:
        conn = get_connection()
        query = """
        SELECT beer_id, brewery_name, style, abv, look, smell, taste, feel, overall,
               average_rating, user_notes, tasted_on
        FROM tasting_journal
        WHERE user_id = ?
        ORDER BY tasted_on DESC
        """
        df = pd.read_sql_query(query, conn, params=(user_id,))
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Failed to load journal: {e}")
        return pd.DataFrame()

def sync_journal_to_db(session_journal, user_id="guest"):
    if not session_journal:
        return 0

    synced = 0
    try:
        conn = get_connection()
        cursor = conn.cursor()

        for entry in session_journal:
            # Avoid duplicates
            cursor.execute("""
                SELECT COUNT(*) FROM tasting_journal
                WHERE user_id = ? AND beer_id = ? AND tasted_on = ?
            """, (user_id, entry["beer_id"], entry["tasted_on"]))
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO tasting_journal (
                        user_id, beer_id, brewery_name, style, abv,
                        look, smell, taste, feel, overall, average_rating,
                        user_notes, tasted_on
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    entry["beer_id"], entry["brewery_name"], entry["style"], entry["abv"],
                    entry["look"], entry["smell"], entry["taste"], entry["feel"], entry["overall"],
                    entry["average_rating"], entry["user_notes"], entry["tasted_on"]
                ))
                synced += 1

        conn.commit()
        conn.close()
        return synced
    except Exception as e:
        st.error(f"❌ Sync failed: {e}")
        return 0

def delete_entry(beer_id, tasted_on, user_id="guest"):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM tasting_journal
            WHERE user_id = ? AND beer_id = ? AND tasted_on = ?
        """, (user_id, beer_id, tasted_on))
        conn.commit()
        conn.close()

        # Remove from session
        st.session_state["journal"] = [
            j for j in st.session_state.get("journal", [])
            if not (j["beer_id"] == beer_id and j["tasted_on"] == tasted_on)
        ]
        st.success(f"🗑️ Deleted entry for '{beer_id}' on {tasted_on}.")
    except Exception as e:
        st.error(f"❌ Delete failed: {e}")

# ------------------------------
# Streamlit Page
# ------------------------------
st.markdown(f"<style>body {{ background-color: {bg_color}; color: {text_color}; }}</style>", unsafe_allow_html=True)
st.markdown(f"<h1>📔 My Tasting Journal</h1>", unsafe_allow_html=True)
st.markdown(f"<p>All your rated beers and notes appear here.</p>", unsafe_allow_html=True)

# -------------------------------
# Load entries from DB and Session
# -------------------------------
session_entries = pd.DataFrame(st.session_state.get("journal", []))
db_entries = load_journal_from_db()

combined_df = pd.concat([db_entries, session_entries], ignore_index=True)
if not combined_df.empty:
    combined_df.drop_duplicates(subset=["beer_id", "tasted_on"], inplace=True)

# -------------------------------
# Sync Button
# -------------------------------
if st.button("💾 Sync Session Journal to Database"):
    synced = sync_journal_to_db(st.session_state.get("journal", []), user_id="guest")
    if synced > 0:
        st.success(f"✅ Synced {synced} new journal entry(ies) to the database.")
    else:
        st.info("All journal entries are already synced.")

# -------------------------------
# Display Journal
# -------------------------------
if combined_df.empty:
    st.info("📝 No entries in your tasting journal yet.")
else:
    csv = combined_df.to_csv(index=False)
    st.download_button("⬇️ Download Journal CSV", csv, "tasting_journal.csv", "text/csv")

    for idx, entry in combined_df.iterrows():
        st.markdown("----")
        st.subheader(f"🍺 {entry['beer_id']} — {entry['brewery_name']}")
        st.caption(f"Tasted on: {entry['tasted_on']}")

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("👀 Look", f"{entry['look']}/5")
        col2.metric("👃 Smell", f"{entry['smell']}/5")
        col3.metric("👅 Taste", f"{entry['taste']}/5")
        col4.metric("🖐️ Feel", f"{entry['feel']}/5")
        col5.metric("⭐ Overall", f"{entry['overall']}/5")

        st.markdown(f"**Avg Rating:** {entry['average_rating']}/5")
        st.markdown(f"**Style:** {entry['style']} | **ABV:** {entry['abv']}%")
        st.markdown(f"**Notes:** {entry['user_notes']}")

        if st.button("🗑️ Delete Entry", key=f"delete_{entry['beer_id']}_{entry['tasted_on']}"):
            delete_entry(entry['beer_id'], entry['tasted_on'])
            st.experimental_rerun()