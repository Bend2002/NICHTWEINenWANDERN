
import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
from storage import init_db, add_user, get_user, get_all_users, assign_team, get_all_teams, reset_password, delete_team

init_db()

STATIONS = [
    {"id": 1, "name": "Westpark", "qr": "station_1_westpark"},
    {"id": 2, "name": "Aussichtspunkt Nord", "qr": "station_2_aussicht"},
    {"id": 3, "name": "Hohlweg", "qr": "station_3_hohlweg"},
    {"id": 4, "name": "Kirschgarten", "qr": "station_4_kirschgarten"},
    {"id": 5, "name": "Hochsitz", "qr": "station_5_hochsitz"},
    {"id": 6, "name": "Rebhang Süd", "qr": "station_6_rebhang"},
    {"id": 7, "name": "Winzerkreuz", "qr": "station_7_kreuz"},
    {"id": 8, "name": "Quellenpfad", "qr": "station_8_quelle"},
    {"id": 9, "name": "Eichenwäldchen", "qr": "station_9_eiche"},
    {"id": 10, "name": "Weingut Zentrale", "qr": "station_10_weingut"},
]

def login():
    st.title("🍷 WanderWinzer Login")
    name = st.text_input("Name")
    password = st.text_input("Passwort (3 Ziffern)", type="password")

    if st.button("Einloggen"):
        user = get_user(name)
        if user and user[2] == password:
            st.session_state["user"] = name
            st.success(f"Willkommen, {name}!")
        else:
            st.error("Login fehlgeschlagen. Benutzername oder Passwort falsch.")

    st.markdown("---")
    st.subheader("Noch kein Konto?")
    new_name = st.text_input("Neuen Namen eingeben")
    new_pass = st.text_input("Neues Passwort (3 Ziffern)", type="password")
    if st.button("Registrieren"):
        if len(new_pass) == 3 and new_pass.isdigit():
            if not get_user(new_name):
                add_user(new_name, new_pass)
                st.success("Registriert! Jetzt einloggen.")
            else:
                st.error("Name bereits vergeben.")
        else:
            st.error("Passwort muss genau 3 Ziffern enthalten.")

def team_builder():
    st.title("🤝 Team bilden")
    users = get_all_users()
    user_names = [u[1] for u in users if u[3] is None]

    col1, col2 = st.columns(2)
    with col1:
        partner1 = st.selectbox("Teammitglied 1", user_names, key="tm1")
    with col2:
        partner2 = st.selectbox("Teammitglied 2", [u for u in user_names if u != partner1], key="tm2")

    if st.button("Team erstellen"):
        assign_team(partner1, partner2)
        st.success(f"Team {partner1} & {partner2} erstellt!")

def admin_panel():
    st.title("🔐 Adminbereich")
    st.subheader("Alle Benutzer")
    users = get_all_users()
    for u in users:
        st.text(f"Name: {u[1]}, Passwort: {u[2]}, Team-ID: {u[3]}")

    st.subheader("Passwort zurücksetzen")
    name = st.text_input("Benutzername für Reset")
    new_pw = st.text_input("Neues Passwort (3 Ziffern)", type="password")
    if st.button("Zurücksetzen"):
        if len(new_pw) == 3 and new_pw.isdigit():
            reset_password(name, new_pw)
            st.success("Passwort aktualisiert")
        else:
            st.error("Ungültiges Passwort")

    st.subheader("Team löschen")
    teams = get_all_teams()
    team_dict = {f"{t[0]}: {t[1]} & {t[2]}": t[0] for t in teams}
    team_sel = st.selectbox("Team wählen", list(team_dict.keys()))
    if st.button("Team löschen"):
        delete_team(team_dict[team_sel])
        st.success("Team gelöscht")

    st.subheader("📷 QR-Codes für Stationen")
    for station in STATIONS:
        st.markdown(f"**{station['name']}**")
        qr_img = qrcode.make(station['qr'])
        buf = BytesIO()
        qr_img.save(buf)
        st.image(Image.open(buf), width=150)
        st.code(station['qr'], language='text')
