# station.py – GPS-Testmodul für Live-Koordinaten
import streamlit as st
from streamlit_javascript import st_javascript

st.title("🧪 GPS Test")

st.write("⏳ Warte auf GPS...")
coords = st_javascript(
    """
    () => {
        return new Promise((resolve) => {
            const watch = navigator.geolocation.watchPosition(
                (pos) => {
                    resolve({ lat: pos.coords.latitude, lon: pos.coords.longitude });
                    navigator.geolocation.clearWatch(watch);
                },
                (err) => {
                    console.warn("Geolocation error:", err);
                    console.log("JS Fehlerdetails:", err);
                    resolve(null);
                },
                { enableHighAccuracy: true }
            );
        });
    }
    """
)

st.write("🔍 Debug: Raw GPS-Daten:", coords)

if coords:
    st.success(f"✅ Standort erhalten:\n\n📍 Latitude: {coords.get('lat')}\n📍 Longitude: {coords.get('lon')}")
else:
    st.warning("❌ Kein Standort verfügbar – bitte Freigabe prüfen und Seite neu laden.")


def station_page():
    st.title("🧪 GPS Test (aus station_page)")
    coords = st_javascript(
        """
        () => {
            return new Promise((resolve) => {
                const watch = navigator.geolocation.watchPosition(
                    (pos) => {
                        resolve({ lat: pos.coords.latitude, lon: pos.coords.longitude });
                        navigator.geolocation.clearWatch(watch);
                    },
                    (err) => {
                        console.warn("Geolocation error:", err);
                        resolve(null);
                    },
                    { enableHighAccuracy: true }
                );
            });
        }
        """
    )
    if coords:
        st.success(f"✅ Standort erhalten:\n\n📍 Latitude: {coords.get('lat')}\n📍 Longitude: {coords.get('lon')}")
    else:
        st.warning("❌ Kein Standort verfügbar – bitte Freigabe prüfen und Seite neu laden.")
