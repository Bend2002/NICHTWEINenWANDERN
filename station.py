# station.py – manuelle Stationswahl + Bewertung mit Adminfreigabe
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


def get_freigegebene_station():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS freigabe (
        id INTEGER PRIMARY KEY,
        station_id INTEGER
    )""")
    c.execute("SELECT station_id FROM freigabe ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row[0] if row else 1


def set_freigegebene_station(station_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM freigabe")
    c.execute("INSERT INTO freigabe (station_id) VALUES (?)", (station_id,))
    conn.commit()
    conn.close()


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
    c.execute("SELECT 1 FROM ratings WHERE user=? AND station_id=?", (user, station_id))
    if c.fetchone():
        conn.close()
        return False  # Bewertung existiert bereits
    c.execute('''INSERT INTO ratings (user, station_id, geschmack, alkohol, kater, kommentar)
                 VALUES (?, ?, ?, ?, ?, ?)''', (user, station_id, geschmack, alkohol, kater, kommentar))
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

    st.markdown(f"### 📍 Aktuelle Station: {station['name']} – {station['wein']}")

    geschmack = st.slider("Geschmack", 0, 10, 5)
    alkohol = st.slider("Geschätzter Alkoholgehalt (%)", 5, 15, 10)
    kater = st.slider("Katergrad", 0, 10, 3)
    kommentar = st.text_area("Bemerkung")

    if st.button("✅ Bewertung speichern"):
        success = save_rating(st.session_state["user"], station["id"], geschmack, alkohol, kater, kommentar)
        if success:
            st.success("Bewertung gespeichert!")
        else:
            st.info("Du hast diese Station bereits bewertet.")

    # Admin kann Station freigeben
    if st.session_state.get("user") == "admin":
        st.markdown("---")
        st.subheader("🔐 Admin: Freigegebene Station setzen")
        new_station = st.selectbox("Nächste Station freigeben", [f"{s['id']}: {s['name']}" for s in STATIONS])
        new_id = int(new_station.split(":" )[0])
        if st.button("🚦 Station freigeben"):
            set_freigegebene_station(new_id)
            st.success(f"Station {new_station} freigegeben!")
