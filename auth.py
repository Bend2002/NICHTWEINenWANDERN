# auth.py – Login, Registrierung, Teamwahl
import streamlit as st
import sqlite3
import os

DB_NAME = os.path.join(os.getcwd(), "wander.db")


def init_user_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            team TEXT DEFAULT ''
        )
    """)
    conn.commit()
    conn.close()


def register_user(username, password, team):
    init_user_table()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, team) VALUES (?, ?, ?)", (username, password, team))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def login_user(username, password):
    init_user_table()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None


def auth_page():
    init_user_table()
    st.title("🔐 Login / Registrierung")

    mode = st.radio("Was möchtest du tun?", ["Einloggen", "Registrieren"])
    username = st.text_input("Benutzername")
    password = st.text_input("Passwort (3 Ziffern)", type="password")

    if mode == "Registrieren":
        team = st.text_input("Teamname")
        if st.button("Registrieren"):
            success = register_user(username, password, team)
            if success:
                st.success("Registrierung erfolgreich. Bitte einloggen.")
            else:
                st.error("Benutzername bereits vergeben.")
    else:
        if st.button("Einloggen"):
            if login_user(username, password):
                st.session_state["user"] = username
                st.query_params["user"] = username
                st.success(f"Willkommen, {username}!")
                st.rerun()
            else:
                st.error("Falsche Login-Daten.")

