# main.py – Navigation & Sessionhandling
import streamlit as st
import os
import sqlite3

from auth import auth_page
from station import station_page

st.set_page_config(page_title="WanderWinzer", page_icon="🍷", layout="centered")

# 📦 Datenbank sicher neu anlegen (nur beim Debuggen nötig)
DB_NAME = os.path.join(os.getcwd(), "wander.db")
if not os.path.exists(DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, team TEXT)")
    conn.commit()
    conn.close()

# 🔐 Persistenter Login über URL ?user=
if "user" not in st.session_state:
    params = st.query_params
    if "user" in params:
        st.session_state["user"] = params["user"][0]

# 📚 Menüstruktur
st.sidebar.title("🍇 Navigation")
menu = st.sidebar.radio("Menü", ["Login", "Wein bewerten"])

# 📍 Seitenlogik
if menu == "Login":
    auth_page()
elif menu == "Wein bewerten":
    station_page()
