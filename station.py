# station.py – manuelle Stationswahl + Bewertung
import streamlit as st
import sqlite3
import os

STATIONS = [
    {"id": 1, "name": "Westpark", "wein": "Wein 1"},
    {"id": 2, "name": "Aussichtspunkt Nord", "wein": "Wein 2"},
    {"id": 3, "name": "Hohlweg", "wein": "Wein 3"},
    {"id": 4, "name": "Kirschgarten", "wein": "Wein 4"},
    {"id": 5, "name": "Hochsitz", "wein": "Wein 5"},
    {"id": 6, "name": "Rebhang Süd", "wein": "Wein 6"},
    {"id": 7, "name": "Winzerkreuz", "wein": "Wein 7"},
    {"id": 8, "name": "Quellenpfad", "wein": "Wein 8"},
    {"id": 9, "name": "Eichenwäldchen", "wein": "Wein 9"},
    {"id": 10, "name": "Weingut Zentrale", "wein": "Wein 10"},
]

DB_NAME = os.path.join(os.getcwd(), "wander.db")


def save_rating(user, station_id, geschmack, alkohol, kater, kommentar):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        station_id INTEGER,
        geschmack INTEGER,
        alkohol INTEGER,
        kater INTEGER,
        kommentar TEXT
    )''')
    c.execute('''INSERT INTO ratings (user, station_id, geschmack, alkohol, kater, kommentar)
                 VALUES (?, ?, ?, ?, ?, ?)''', (user, station_id, geschmack, alkohol, kater, kommentar))
    conn.commit()
    conn.close()


def station_page():
    st.title("🍷 Wein bewerten")

    if "user" not in st.session_state:
        st.warning("Bitte zuerst einloggen.")
        return

    station_names = [f"{s['id']}: {s['name']} ({s['wein']})" for s in STATIONS]
    selection = st.selectbox("Wähle deine aktuelle Station", station_names)
    station_id = int(selection.split(":")[0])
    station = next(s for s in STATIONS if s["id"] == station_id)

    st.markdown(f"### 📍 {station['name']} – {station['wein']}")

    geschmack = st.slider("Geschmack", 0, 10, 5)
    alkohol = st.slider("Geschätzter Alkoholgehalt (%)", 5, 15, 10)
    kater = st.slider("Katergrad", 0, 10, 3)
    kommentar = st.text_area("Bemerkung")

    if st.button("✅ Bewertung speichern"):
        save_rating(st.session_state["user"], station_id, geschmack, alkohol, kater, kommentar)
        st.success("Bewertung gespeichert!")
