# main.py
import streamlit as st
from auth import login, team_builder, admin_panel

# Startseite
st.set_page_config(page_title="WanderWinzer", page_icon="🍷", layout="centered")

if "user" not in st.session_state:
    login()
else:
    st.sidebar.title("Navigation")
    st.sidebar.markdown(f"👤 Eingeloggt als: {st.session_state['user']}")

    selection = st.sidebar.radio("Wähle eine Seite:", ["Team bilden", "Adminbereich", "Logout"])

    if selection == "Team bilden":
        team_builder()

    elif selection == "Adminbereich":
        if st.session_state["user"].lower() == "admin":
            admin_panel()
        else:
            st.warning("Nur Admin hat Zugriff auf diesen Bereich.")

    elif selection == "Logout":
        del st.session_state["user"]
        st.experimental_rerun()
