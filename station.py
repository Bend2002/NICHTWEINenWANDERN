# station.py
import streamlit as st
import math
import sqlite3
import os
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# Dummy-Datenbank der Stationen
STATIONS = [
    {"id": 1, "name": "Westpark", "qr": "station_1_westpark", "lat": 50.771999, "lon": 6.070250, "wein": "Wein 1"},
    {"id": 2, "name": "Aussichtspunkt Nord", "qr": "station_2_aussicht", "lat": 50.805222, "lon": 5.960278, "wein": "Wein 2"},
    {"id": 3, "name": "Hohlweg", "qr": "station_3_hohlweg", "lat": 50.780000, "lon": 6.030000, "wein": "Wein 3"},
    {"id": 4, "name": "Kirschgarten", "qr": "station_4_kirschgarten", "lat": 50.782000, "lon": 6.015000, "wein": "Wein 4"},
    {"id": 5, "name": "Hochsitz", "qr": "station_5_hochsitz", "lat": 50.785000, "lon": 6.002000, "wein": "Wein 5"},
    {"id": 6, "name": "Rebhang Süd", "qr": "station_6_rebhang", "lat": 50.790000, "lon": 5.990000, "wein": "Wein 6"},
    {"id": 7, "name": "Winzerkreuz", "qr": "station_7_kreuz", "lat": 50.795000, "lon": 5.980000, "wein": "Wein 7"},
    {"id": 8, "name": "Quellenpfad", "qr": "station_8_quelle", "lat": 50.800000, "lon": 5.970000, "wein": "Wein 8"},
    {"id": 9, "name": "Eichenwäldchen", "qr": "station_9_eiche", "lat": 50.803000, "lon": 5.965000, "wein": "Wein 9"},
    {"id": 10, "name": "Weingut Zentrale", "qr": "station_10_weingut", "lat": 50.808000, "lon": 5.960000, "wein": "Wein 10"},
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

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def station_page():
    st.title("📍 Station entdecken")

    if "user" not in st.session_state:
        st.warning("Bitte zuerst einloggen.")
        return

    qr_input = st.text_input("QR-Code-Inhalt eingeben")

    st.markdown("### 📡 Aktueller Standort (live über Browser)")
    components.html("""
    <script>
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const latitude = pos.coords.latitude.toFixed(6);
        const longitude = pos.coords.longitude.toFixed(6);
        const streamlitDoc = window.parent.document;
        streamlitDoc.querySelector('input[data-baseweb="input"]:nth-of-type(1)').value = latitude;
        streamlitDoc.querySelector('input[data-baseweb="input"]:nth-of-type(2)').value = longitude;
        streamlitDoc.querySelector('input[data-baseweb="input"]:nth-of-type(1)').dispatchEvent(new Event('input'));
        streamlitDoc.querySelector('input[data-baseweb="input"]:nth-of-type(2)').dispatchEvent(new Event('input'));
      },
      (err) => alert('GPS nicht verfügbar: ' + err.message)
    );
    </script>
    """, height=0)

    user_lat = st.number_input("📍 Latitude", format="%.6f")
    user_lon = st.number_input("📍 Longitude", format="%.6f")

    station = next((s for s in STATIONS if s["qr"] == qr_input), None)

    if station:
        st.success(f"Gefunden: {station['name']} – {station['wein']}")

        st.markdown("### 🧪 Bewertung")
        geschmack = st.slider("Geschmack", 0, 10, 5)
        alkohol = st.slider("Geschätzter Alkoholgehalt (%)", 5, 15, 10)
        kater = st.slider("Katergrad", 0, 10, 3)
        kommentar = st.text_area("Bemerkung")

        if st.button("Bewertung speichern"):
            save_rating(
                st.session_state["user"],
                station["id"],
                geschmack,
                alkohol,
                kater,
                kommentar
            )
            st.success("Bewertung gespeichert ✅")

        st.markdown("### 🧭 Nächste Station")
        idx = station['id'] - 1
        if idx + 1 < len(STATIONS):
            next_station = STATIONS[idx + 1]
            dist = haversine(user_lat, user_lon, next_station['lat'], next_station['lon'])
            st.info(f"Nächste Station: {next_station['name']}")
            st.metric(label="Entfernung", value=f"{dist:.2f} km")
        else:
            st.success("🍾 Ziel erreicht! Das war die letzte Station.")
    elif qr_input:
        st.error("Ungültiger QR-Code")
