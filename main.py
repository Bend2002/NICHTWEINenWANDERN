
import streamlit as st
from auth import login, team_builder, admin_panel
from station import station_page
from match import match_page
from leaderboard import leaderboard_page
from task import task_page
from storage import init_db

# Initialisiere Datenbank (nur beim Start)
init_db()

# Startseite
st.set_page_config(page_title="WanderWinzer", page_icon="🍷", layout="centered")

if "user" not in st.session_state:
    login()
else:
    st.sidebar.title("Navigation")
    st.sidebar.markdown(f"👤 Eingeloggt als: {st.session_state['user']}")

    selection = st.sidebar.radio("Wähle eine Seite:", [
        "Station entdecken",
        "Aufgabe erledigen",
        "Team bilden",
        "Matching anzeigen",
        "Leaderboard",
        "Adminbereich",
        "Logout"
    ])

    if selection == "Station entdecken":
        station_page()

    elif selection == "Aufgabe erledigen":
        task_page()

    elif selection == "Team bilden":
        team_builder()

    elif selection == "Matching anzeigen":
        match_page()

    elif selection == "Leaderboard":
        leaderboard_page()

    elif selection == "Adminbereich":
        if st.session_state["user"].lower() == "admin":
            admin_panel()
        else:
            st.warning("Nur Admin hat Zugriff auf diesen Bereich.")

    elif selection == "Logout":
        del st.session_state["user"]
        st.experimental_rerun()
