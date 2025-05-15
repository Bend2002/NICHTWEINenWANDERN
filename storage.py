
import sqlite3

DB_NAME = "data/wander.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        password TEXT NOT NULL,
        team_id INTEGER
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member1 TEXT,
        member2 TEXT
    )''')

    conn.commit()
    conn.close()

def add_user(name, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, password))
    conn.commit()
    conn.close()

def get_user(name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name = ?", (name,))
    user = c.fetchone()
    conn.close()
    return user

def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return users

def assign_team(user1, user2):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO teams (member1, member2) VALUES (?, ?)", (user1, user2))
    team_id = c.lastrowid
    c.execute("UPDATE users SET team_id = ? WHERE name IN (?, ?)", (team_id, user1, user2))
    conn.commit()
    conn.close()

def get_all_teams():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM teams")
    teams = c.fetchall()
    conn.close()
    return teams

def reset_password(name, new_password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE name = ?", (new_password, name))
    conn.commit()
    conn.close()

def delete_team(team_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM teams WHERE id = ?", (team_id,))
    c.execute("UPDATE users SET team_id = NULL WHERE team_id = ?", (team_id,))
    conn.commit()
    conn.close()
