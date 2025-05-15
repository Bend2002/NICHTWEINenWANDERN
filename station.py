# station.py – Weinbewertung je Station
import streamlit as st
import sqlite3
import os

DB_NAME = os.path.join(os.getcwd(), "wander.db")

STATIONS = [
    {"id": 1, "name": "Westpark", "wein": "Wein 1"},
    {"id": 2, "name": "Aussichtspunkt Nord", "wein": "Wein 2"},
    {"id": 3, "name": "Kirschgarten", "wein": "Wein 3"},
    {"id": 4, "name": "Weingut Finale", "wein": "Wein 4"},
]


# aktuelle station, die bewertet werden darf (admin setzt)
def get_freigegebene_station():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS freigabe (
            id INTEGER PRIMARY KEY,
            station_id INTEGER
        )""")
    c.execute("SELECT station_id FROM freigabe ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row[0] if row else 1


def save_rating(user, station_id, geschmack, preis, rebsorte, alkohol, kater, kommentar):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            station_id INTEGER,
            geschmack INTEGER,
            preis INTEGER,
            rebsorte TEXT,
            alkohol INTEGER,
            kater INTEGER,
            kommentar TEXT
        )""")
    c.execute("SELECT 1 FROM ratings WHERE user=? AND station_id=?", (user, station_id))
    if c.fetchone():
        conn.close()
        return False
    c.execute("""
        INSERT INTO ratings (user, station_id, geschmack, preis, rebsorte, alkohol, kater, kommentar)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (user, station_id, geschmack, preis, rebsorte, alkohol, kater, kommentar))
    conn.commit()
    conn.close()
    return True


def station_page():
    st.title("🍷 Wein bewerten")
    if "user" not in st.session_state:
        st.warning("Bitte zuerst einloggen.")
        return

    current_station_id = get_freigegebene_station()
    station = next(s for s in STATIONS if s["id"] == current_station_id)

    st.subheader(f"📍 {station['name']} – {station['wein']}")

    geschmack = st.slider("Wie hat der Wein geschmeckt?", 0, 10, 5, format="%d",
        help="0 = Plörre, 10 = Göttlich")
    preis = st.number_input("Was denkst du, kostet die Flasche (in €)?", min_value=0, max_value=200)
    rebsorte = st.selectbox("Welche Rebsorte vermutest du?", ["Riesling", "Spätburgunder", "Grauburgunder", "Silvaner", "Dornfelder", "Andere"])
    alkohol = st.slider("Wie stark ballert der?", 5, 15, 10, format="%d %%",
        help="5 % = Frühstückswein, 15 % = Endgegner")
    kater = st.slider("Wie fühlt sich dein Kopp morgen an?", 0, 10, 3,
        help="0 = läuft, 10 = auaaa")
    kommentar = st.text_area("Freie Gedanken")

    if st.button("✅ Bewertung abschicken"):
        ok = save_rating(
            st.session_state["user"], current_station_id,
            geschmack, preis, rebsorte, alkohol, kater, kommentar
        )
        if ok:
            st.success("Bewertung gespeichert!")
        else:
            st.info("Du hast diese Station bereits bewertet.")
