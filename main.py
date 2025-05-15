# main.py – Navigation & Sessionhandling
import streamlit as st
import os
import sqlite3

from auth import auth_page
from station import station_page
from leaderboard import leaderboard_page
from rating import rating_page
from admin import admin_page

st.set_page_config(page_title="WanderWinzer", page_icon="🍷", layout="centered")

# 📦 Datenbank vorbereiten (nur beim ersten Start)
DB_NAME = os.path.join(os.getcwd(), "wander.db")
if not os.path.exists(DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            team TEXT DEFAULT ''
        )
    """)
    conn.commit()
    conn.close()

# 🔐 Persistenter Login über ?user=... aus URL
if "user" not in st.session_state:
    params = st.query_params
    if "user" in params:
        st.session_state["user"] = params["user"][0]

# 📚 Navigation
st.sidebar.title("🍇 WanderWinzer Menü")
menu = st.sidebar.radio("Wähle eine Seite:", ["Login", "Wein bewerten", "Mein Geschmack", "Leaderboard", "Admin"])

# 📍 Seitenrouting
if menu == "Login":
    auth_page()
elif menu == "Wein bewerten":
    station_page()
elif menu == "Mein Geschmack":
    rating_page()
elif menu == "Leaderboard":
    leaderboard_page()
elif menu == "Admin":
    admin_page()
