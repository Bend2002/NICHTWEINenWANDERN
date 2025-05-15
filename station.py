# station.py
import streamlit as st
import math
import sqlite3
import os
import numpy as np
import matplotlib.pyplot as plt
from streamlit_javascript import st_javascript

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


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def bearing(lat1, lon1, lat2, lon2):
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_lon = math.radians(lon2 - lon1)
    y = math.sin(delta_lon) * math.cos(phi2)
    x = math.cos(phi1)*math.sin(phi2) - math.sin(phi1)*math.cos(phi2)*math.cos(delta_lon)
    brng = math.atan2(y, x)
    return (math.degrees(brng) + 360) % 360


def draw_arrow(angle):
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.arrow(0.5, 0.5, 0.3 * math.cos(math.radians(angle)), 0.3 * math.sin(math.radians(angle)),
             head_width=0.05, head_length=0.05, fc='red', ec='black')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    st.pyplot(fig)


def station_page():
    st.title("📍 Station entdecken")

    if "user" not in st.session_state:
        st.warning("Bitte zuerst einloggen.")
        return

    qr_input = st.text_input("QR-Code-Inhalt eingeben")

    st.markdown("### 📡 Aktueller Standort (live per GPS)")

    coords = st_javascript(
        """
        async () => {
            const pos = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject, { enableHighAccuracy: true });
            });
            return { lat: pos.coords.latitude, lon: pos.coords.longitude };
        }
        """
    )

    user_lat = coords.get("lat", 0.0) if coords else 0.0
    user_lon = coords.get("lon", 0.0) if coords else 0.0

    st.write(f"📍 Deine Koordinaten: **{user_lat:.6f}**, **{user_lon:.6f}**")
