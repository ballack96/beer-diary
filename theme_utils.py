import streamlit as st

# Dark Theme CSS
dark_mode_css = """
<style>
/* Main app background and text */
.stApp {
    background-color: #262730;
    color: #FFFFFF;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1E1E1E;
    color: #FFFFFF;
}

/* Cards and containers */
div.stButton > button {
    background-color: #4E4E50;
    color: white;
}

/* Inputs */
div.stTextInput > div > div > input {
    background-color: #3A3A3A;
    color: white;
}

/* Dataframe */
.stDataFrame {
    background-color: #2C2C2C;
}
div.stDataFrame > div > div > div > div > div table {
    color: white;
}

/* Expander */
.streamlit-expanderHeader {
    background-color: #3A3A3A;
    color: white;
}

/* Slider */
.stSlider > div > div {
    background-color: #4E4E50;
}

/* Text area */
.stTextArea > div > div > textarea {
    background-color: #3A3A3A;
    color: white;
}

/* Metric */
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
    color: #FFFFFF;
}

/* Select boxes */
div.stSelectbox > div > div > div {
    background-color: #3A3A3A;
    color: white;
}

/* Multiselect */
div.stMultiSelect > div > div > div {
    background-color: #3A3A3A;
    color: white;
}

/* Radio buttons */
.stRadio > div {
    color: white;
}

/* Checkboxes */
.stCheckbox > div {
    color: white;
}

/* Number input */
div.stNumberInput > div > div > input {
    background-color: #3A3A3A;
    color: white;
}

/* Date input */
div.stDateInput > div > div > input {
    background-color: #3A3A3A;
    color: white;
}
</style>
"""

# Light Theme CSS
light_mode_css = """
<style>
/* Main app background and text */
.stApp {
    background-color: #FFFFFF;
    color: #262730;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #F0F2F6;
    color: #262730;
}

/* Cards and containers */
div.stButton > button {
    background-color: #FAFAFA;
    color: #262730;
    border: 1px solid #CCCCCC;
}

/* Inputs */
div.stTextInput > div > div > input {
    background-color: #FFFFFF;
    color: #262730;
    border: 1px solid #CCCCCC;
}

/* Dataframe */
.stDataFrame {
    background-color: #FFFFFF;
}
div.stDataFrame > div > div > div > div > div table {
    color: #262730;
}

/* Expander */
.streamlit-expanderHeader {
    background-color: #F0F2F6;
    color: #262730;
}

/* Slider */
.stSlider > div > div {
    background-color: #E0E0E0;
}

/* Text area */
.stTextArea > div > div > textarea {
    background-color: #FFFFFF;
    color: #262730;
    border: 1px solid #CCCCCC;
}

/* Metric */
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
    color: #262730;
}

/* Select boxes */
div.stSelectbox > div > div > div {
    background-color: #FFFFFF;
    color: #262730;
}

/* Multiselect */
div.stMultiSelect > div > div > div {
    background-color: #FFFFFF;
    color: #262730;
}

/* Radio buttons */
.stRadio > div {
    color: #262730;
}

/* Checkboxes */
.stCheckbox > div {
    color: #262730;
}

/* Number input */
div.stNumberInput > div > div > input {
    background-color: #FFFFFF;
    color: #262730;
}

/* Date input */
div.stDateInput > div > div > input {
    background-color: #FFFFFF;
    color: #262730;
}
</style>
"""

def apply_theme():
    """Apply the current theme based on session state"""
    # Set default theme if not present
    if 'theme' not in st.session_state:
        st.session_state.theme = "Light"
    
    # Theme toggle that maintains state across pages
    theme = st.sidebar.radio("🌓 Theme", ["Light", "Dark"], 
                            horizontal=True, 
                            index=0 if st.session_state.theme == "Light" else 1,
                            key="theme_toggle")
    
    # Update session state when changed
    if theme != st.session_state.theme:
        st.session_state.theme = theme
    
    # Apply the appropriate CSS
    if st.session_state.theme == "Dark":
        st.markdown(dark_mode_css, unsafe_allow_html=True)
    else:
        st.markdown(light_mode_css, unsafe_allow_html=True)
    
    # Return the theme for use in charts like Plotly
    return st.session_state.theme