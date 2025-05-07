import streamlit as st

# Theme toggle (visible in sidebar)
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "light"

selected_theme = st.sidebar.radio("🌗 Theme", ["light", "dark"], index=0 if st.session_state["theme_mode"] == "light" else 1)
st.session_state["theme_mode"] = selected_theme

def get_app_theme():
    theme_mode = st.session_state.get("theme_mode", "light")

    if theme_mode == "dark":
        bg_color = "#0e1117"
        text_color = "#f1f1f1"
        sidebar_color = "#161b22"
        card_color = "#1f2937"
        plotly_template = "plotly_dark"
    else:
        bg_color = "#ffffff"
        text_color = "#000000"
        sidebar_color = "#f0f2f6"
        card_color = "#ffffff"
        plotly_template = "plotly_white"

    # Apply background and text color via HTML
    st.markdown(f"<style>body {{ background-color: {bg_color}; color: {text_color}; }}</style>", unsafe_allow_html=True)

    return bg_color, text_color, sidebar_color, card_color, plotly_template
