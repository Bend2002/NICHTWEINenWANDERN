# admin.py – Adminsteuerung: Station freigeben, Teams verwalten
import streamlit as st
import sqlite3
import os
import pandas as pd

DB_NAME = os.path.join(os.getcwd(), "wander.db")
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)
    st.warning("❌ Datenbank wurde gelöscht. Bitte App neu laden.")

STATIONS = [
    {"id": 1, "name": "Westpark"},
    {"id": 2, "name": "Aussichtspunkt Nord"},
    {"id": 3, "name": "Kirschgarten"},
    {"id": 4, "name": "Weingut Finale"},
]


def admin_page():
    st.title("🔧 Adminbereich")

    st.subheader("📍 Station freigeben")
    selected = st.selectbox("Welche Station soll aktiv sein?", options=STATIONS, format_func=lambda s: f"{s['id']}: {s['name']}")
    if st.button("Freigeben"):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS freigabe (id INTEGER PRIMARY KEY, station_id INTEGER)")
        c.execute("INSERT INTO freigabe (station_id) VALUES (?)", (selected["id"],))
        conn.commit()
        conn.close()
        st.success(f"Station {selected['name']} ist jetzt freigegeben!")

    st.subheader("👥 Benutzerverwaltung")
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT username, team FROM users", conn)
    conn.close()

    if df.empty:
        st.info("Noch keine Benutzer registriert.")
    else:
        st.dataframe(df)

        user_to_delete = st.selectbox("Benutzer löschen", df["username"].tolist())
        if st.button("Löschen"):
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE username = ?", (user_to_delete,))
            conn.commit()
            conn.close()
            st.success(f"Benutzer {user_to_delete} gelöscht.")
            st.rerun()
