
import streamlit as st
import sqlite3
import pandas as pd
from scipy.spatial.distance import euclidean
from itertools import combinations

DB_NAME = "data/wander.db"

def fetch_ratings():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT user, station_id, geschmack, alkohol, kater FROM ratings", conn)
    conn.close()
    return df

def compute_similarity_matrix(df):
    users = df["user"].unique()
    profiles = {}

    for user in users:
        user_df = df[df["user"] == user].sort_values("station_id")
        vec = user_df[["geschmack", "alkohol", "kater"]].values.flatten()
        profiles[user] = vec

    scores = []
    for u1, u2 in combinations(users, 2):
        v1 = profiles.get(u1)
        v2 = profiles.get(u2)
        if len(v1) == len(v2):
            dist = euclidean(v1, v2)
            similarity = 1 / (1 + dist)
            scores.append((u1, u2, round(similarity * 100, 2)))

    return sorted(scores, key=lambda x: x[2], reverse=True)

def match_page():
    st.title("💞 Geschmackspartner finden")

    df = fetch_ratings()
    if df.empty:
        st.info("Noch keine Bewertungen vorhanden.")
        return

    scores = compute_similarity_matrix(df)
    if not scores:
        st.warning("Nicht genug Daten für Matching.")
        return

    st.subheader("Top Geschmackspaare")
    for u1, u2, score in scores[:5]:
        st.write(f"**{u1}** & **{u2}** – {score}% Übereinstimmung")

    if "user" in st.session_state:
        user_matches = [(u1, u2, s) for u1, u2, s in scores if st.session_state["user"] in (u1, u2)]
        if user_matches:
            best_match = user_matches[0]
            partner = best_match[1] if best_match[0] == st.session_state["user"] else best_match[0]
            st.success(f"💡 Dein bester Geschmackspartner ist **{partner}** mit {best_match[2]}% Übereinstimmung!")
