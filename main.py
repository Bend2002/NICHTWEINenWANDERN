# main.py – Navigation & Sessionhandling
import streamlit as st
from station import station_page
from auth import auth_page

st.set_page_config(page_title="WanderWinzer", page_icon="🍷", layout="centered")

# Persistente Anmeldung über URL ?user=
if "user" not in st.session_state:
    params = st.query_params
    if "user" in params:
        st.session_state["user"] = params["user"][0]

# Menüstruktur
st.sidebar.title("🍇 Navigation")
menu = st.sidebar.radio("Menü", ["Login", "Wein bewerten"])

# Seitenlogik
if menu == "Login":
    auth_page()
elif menu == "Wein bewerten":
    station_page()
