# leaderboard.py – Teamranking nach Aufgabenbewertung
import streamlit as st
import sqlite3
import os
import pandas as pd

DB_NAME = os.path.join(os.getcwd(), "wander.db")


def get_team_scores():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Stelle sicher, dass es Teams gibt
    c.execute("SELECT username, team FROM users")
    team_map = dict(c.fetchall())

    df = pd.read_sql_query("SELECT user, station_id, geschmack FROM ratings", conn)
    df["team"] = df["user"].map(team_map)

    # Mittelwert pro Team berechnen
    team_scores = df.groupby("team")["geschmack"].mean().reset_index()
    team_scores = team_scores.sort_values("geschmack", ascending=False)

    # Teammitglieder anzeigen
    members = pd.DataFrame(team_map.items(), columns=["user", "team"])
    conn.close()
    return team_scores, members


def leaderboard_page():
    st.title("🏆 Teamranking")

    team_scores, members = get_team_scores()
    if team_scores.empty:
        st.info("Noch keine Bewertungen vorhanden.")
        return

    for i, row in team_scores.iterrows():
        st.markdown(f"### 🥇 {row['team']}: Ø {round(row['geschmack'],1)}")
        user_list = members[members["team"] == row["team"]]["user"].tolist()
        st.caption("👥 " + ", ".join(user_list))
