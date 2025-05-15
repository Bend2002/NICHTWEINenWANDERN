
import streamlit as st
import sqlite3
import pandas as pd

DB_NAME = "data/wander.db"

def fetch_teams():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM teams", conn)
    conn.close()
    return df

def fetch_points():
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
    df = pd.read_sql_query("SELECT * FROM tasks", conn)
    conn.close()
    return df

def leaderboard_page():
    st.title("🏆 Team-Rangliste")

    teams_df = fetch_teams()
    points_df = fetch_points()

    if teams_df.empty:
        st.info("Noch keine Teams vorhanden.")
        return

    summary = points_df.groupby("team_id")["punkte"].sum().reset_index()
    summary = summary.merge(teams_df, left_on="team_id", right_on="id")
    summary = summary.sort_values("punkte", ascending=False)

    for _, row in summary.iterrows():
        st.markdown(f"**{row['member1']} & {row['member2']}** – {row['punkte']} Punkte")

    if "user" in st.session_state:
        my_team = teams_df[(teams_df["member1"] == st.session_state["user"]) | (teams_df["member2"] == st.session_state["user"])]
        if not my_team.empty:
            team_id = my_team.iloc[0]["id"]
            team_points = summary[summary["team_id"] == team_id]["punkte"].values[0] if team_id in summary["team_id"].values else 0
            st.success(f"🎯 Dein Team hat aktuell {team_points} Punkte!")
