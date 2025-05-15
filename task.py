# task.py – Team-Aufgaben pro Station
import streamlit as st
import sqlite3
import os

DB_NAME = os.path.join(os.getcwd(), "wander.db")

# Aufgabenbank pro Station
AUFGABEN = {
    1: "Wie viele Trauben sind ca. nötig für eine Flasche?",
    2: "Was denkst du: Wie viel Alkohol hat der Wein?",
    3: "Wie viele Jahre alt ist der Wein?",
    4: "Wie viele Kalorien hat ein Glas von diesem Wein?",
}

def save_team_solution(teamname, station_id, antwort):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS aufgaben (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team TEXT,
            station_id INTEGER,
            antwort TEXT
        )
    """)
    c.execute("SELECT 1 FROM aufgaben WHERE team = ? AND station_id = ?", (teamname, station_id))
    if c.fetchone():
        conn.close()
        return False

    c.execute("INSERT INTO aufgaben (team, station_id, antwort) VALUES (?, ?, ?)",
              (teamname, station_id, antwort))
    conn.commit()
    conn.close()
    return True


def task_page():
    st.title("👯‍♂️ Team-Aufgabe")
    if "user" not in st.session_state:
        st.warning("Bitte zuerst einloggen.")
        return

    # Teamname ermitteln
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT team FROM users WHERE username = ?", (st.session_state["user"],))
    row = c.fetchone()
    conn.close()
    if not row:
        st.error("Kein Team gefunden.")
        return
    teamname = row[0]

    # Aktuelle Station aus freigabe-Tabelle lesen
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT station_id FROM freigabe ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    if not row:
        st.error("Keine Station freigegeben.")
        return
    station_id = row[0]

    frage = AUFGABEN.get(station_id, "Aufgabe für diese Station folgt bald...")
    st.subheader(frage)

    antwort = st.text_input("Antwort eingeben")
    if st.button("Antwort absenden"):
        if save_team_solution(teamname, station_id, antwort):
            st.success("Antwort gespeichert für dein Team!")
        else:
            st.info("Dein Team hat für diese Station schon geantwortet.")
