# rating.py – Matching + Lieblingswein
import streamlit as st
import sqlite3
import os
import pandas as pd

DB_NAME = os.path.join(os.getcwd(), "wander.db")


def get_user_ratings(user):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM ratings WHERE user = ?", conn, params=(user,))
    conn.close()
    return df


def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT DISTINCT user FROM ratings", conn)
    conn.close()
    return df["user"].tolist()


def calculate_similarity(user1_df, user2_df):
    merged = pd.merge(user1_df, user2_df, on="station_id", suffixes=("_1", "_2"))
    if merged.empty:
        return 0
    return -((merged["geschmack_1"] - merged["geschmack_2"])**2).mean()


def best_wine(df):
    if df.empty:
        return None
    best = df.sort_values("geschmack", ascending=False).iloc[0]
    return best


def rating_page():
    st.title("💘 Mein Weingeschmack")
    if "user" not in st.session_state:
        st.warning("Bitte zuerst einloggen.")
        return

    user = st.session_state["user"]
    df = get_user_ratings(user)

    if df.empty:
        st.info("Du hast noch keinen Wein bewertet.")
        return

    st.subheader("📊 Deine Bewertungen")
    st.dataframe(df[["station_id", "geschmack", "rebsorte", "alkohol"]])

    # 🔍 Lieblingswein
    fav = best_wine(df)
    if fav is not None:
        st.success(f"Dein bisheriger Favorit: Station {fav['station_id']} – Note {fav['geschmack']}/10")

    # 🤝 Matching-Partner
    best_match = None
    best_score = -float("inf")

    all_users = get_all_users()
    for other in all_users:
        if other == user:
            continue
        score = calculate_similarity(df, get_user_ratings(other))
        if score > best_score:
            best_score = score
            best_match = other

    if best_match:
        st.info(f"👯‍♂️ Dein Wein-Zwilling: {best_match} (Ähnlichkeit: {round(best_score,2)})")
