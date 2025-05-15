import streamlit as st
import sqlite3

import os
DB_NAME = os.path.join(os.getcwd(), "wander.db")


def init_task_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_id INTEGER,
        station_id INTEGER,
        aufgabe TEXT,
        loesung TEXT,
        punkte INTEGER
    )''')
    conn.commit()
    conn.close()

def save_task_result(team_id, station_id, aufgabe, loesung, punkte):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO tasks (team_id, station_id, aufgabe, loesung, punkte)
        VALUES (?, ?, ?, ?, ?)
    """, (team_id, station_id, aufgabe, loesung, punkte))
    conn.commit()
    conn.close()

def task_page():
    st.title("🧩 Wein-Aufgabe")

    if "user" not in st.session_state:
        st.warning("Bitte zuerst einloggen.")
        return

    station_id = st.number_input("Station-ID", min_value=1, max_value=10, step=1)
    aufgabe = st.text_area("Aufgabe eingeben (z. B. Schätzfrage, Quiz etc.)")
    loesung = st.text_input("Lösung (freiwillig)")
    punkte = st.slider("Punkte (0–10)", 0, 10, 5)

    if st.button("Aufgabe abspeichern"):
        # Team-ID herausfinden
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT team_id FROM users WHERE name = ?", (st.session_state["user"],))
        result = c.fetchone()
        conn.close()

        if result:
            team_id = result[0]
            save_task_result(team_id, station_id, aufgabe, loesung, punkte)
            st.success("Aufgabe erfolgreich gespeichert ✅")
        else:
            st.error("Kein Team gefunden. Bitte Team bilden.")

# Datenbank initialisieren beim Laden
init_task_db()
