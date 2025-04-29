# 🍻 Beer Diary

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://beer-diary.streamlit.app/)

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)](#)

---

A **Craft Beer Exploration and Tasting Journal** built with **Streamlit** and **SQLite** —  
for beer enthusiasts to discover, rate, and track their tasting experiences!

---

## 🚀 Features

- 🗺️ **Brewery Locator** (Live Map)  
- 🍺 **Beer Explorer** using real beers dataset (Kaggle-based)  
- 📔 **Tasting Journal** (Rate Look, Smell, Taste, Feel, Overall)  
- 🔎 **Style and ABV Filters** for personalized discovery  
- 🎯 **Color-coded Rating Badges** (Excellent, Good, Average, Poor)  
- 📥 **Export Tasting Journal to CSV**  
- 📊 (Coming Soon) **Top Rated Beers Leaderboard**

---

## 🛠 Tech Stack

- [Streamlit](https://streamlit.io/) — Frontend UI
- [SQLite3](https://sqlite.org/) — Local database
- [Pandas](https://pandas.pydata.org/) — Data processing
- [Plotly](https://plotly.com/python/) — (Optional) Future visual analytics
- Python 3.11+

---

## 📦 Installation

```bash
# 1. Clone the repo
git clone https://github.com/ballack96/beer-diary.git
cd beer-diary

# 2. (Optional) Create a virtual environment
python -m venv venv
# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize the database
python init_db.py

# 5. Run the Streamlit app
streamlit run app.py
