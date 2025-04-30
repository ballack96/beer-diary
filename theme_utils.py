# theme_utils.py
import streamlit as st
from streamlit_theme import st_theme

def get_current_theme():
    theme = st_theme()
    if theme is None:
        # Fallback to default light theme settings
        return {
            "base": "light",
            "primaryColor": "#1f77b4",
            "backgroundColor": "#ffffff",
            "secondaryBackgroundColor": "#f0f2f6",
            "textColor": "#262730",
            "font": "sans serif"
        }
    return theme

def get_app_theme():
    theme = st_theme()
    if theme is None:
        return "light", "#000", "#fff", "#f5f5f5", "plotly_white"
    
    base = theme.get("base", "light")
    text_color = "#000000" if base == "light" else "#FFFFFF"
    bg_color = "#ffffff" if base == "light" else "#1c1c1c"
    secondary_bg = "#f7f7f7" if base == "light" else "#2a2a2a"
    plotly_template = "plotly_white" if base == "light" else "plotly_dark"

    return base, text_color, bg_color, secondary_bg, plotly_template

# def get_app_theme():
#     theme = get_theme()
#     base = theme.get("base", "light")
#     text_color = "#222" if base == "light" else "#f0f0f0"
#     bg_color = "#ffffff" if base == "light" else "#1c1c1c"
#     secondary_bg = "#f7f7f7" if base == "light" else "#2a2a2a"
#     plotly_template = "plotly_white" if base == "light" else "plotly_dark"
#     return base, text_color, bg_color, secondary_bg, plotly_template
