import os
import time
import requests
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sgp4.api import Satrec, jday
from sklearn.ensemble import IsolationForest
from dotenv import load_dotenv

# -----------------------------
# CONFIG
# -----------------------------
load_dotenv()
NASA_API_KEY = os.getenv("NASA_API_KEY")

st.set_page_config(layout="wide")
st.title("🛰️ AI Space Surveillance System (Asteroids + Satellites)")

# Sidebar controls
st.sidebar.header("Controls")
refresh_sec = st.sidebar.slider("Auto-refresh (seconds)", 5, 60, 15, 5)
steps = st.sidebar.slider("Orbit steps (minutes ahead)", 20, 200, 80, 10)
num_sats = st.sidebar.slider("Number of satellites", 1, 10, 5, 1)

# -----------------------------
# 1) ASTEROIDS (NASA NEO)
# -----------------------------
@st.cache_data(ttl=300)
def get_asteroids(api_key: str) -> pd.DataFrame:
    url = f"https://api.nasa.gov/neo/rest/v1/feed?api_key={api_key}"
    data = requests.get(url, timeout=15).json()

    rows = []
    for date in data.get('near_earth_objects', {}):
        for obj in data['near_earth_objects'][date]:
            cad = obj.get('close_approach_data', [])
            if not cad:
                continue
            vel = float(cad[0]['relative_velocity']['kilometers_per_hour'])
            rows.append({
                "name": obj['name'],
                "velocity_kmph": vel,
                "hazardous": obj['is_potentially_hazardous_asteroid']
            })
    return pd.DataFrame(rows)

# -----------------------------
# 2) TLE (CelesTrak)
# -----------------------------
@st.cache_data(ttl=600)
def get_tle(n: int):
    url = "https://celestrak.org/NORAD/elements/stations.txt"
    lines = requests.get(url, timeout=15).text.split("\n")
    sats = []
    for i in range(0, len(lines)-2, 3):
        name = lines[i].strip()
        l1 = lines[i+1].strip()
        l2 = lines[i+2].strip()
        if name and l1 and l2:
            sats.append((name, l1, l2))
        if len(sats) >= n:
            break
    return sats

# -----------------------------
# 3) PROPAGATION (SGP4)
# -----------------------------
def propagate(l1, l2, steps=80):
    sat = Satrec.twoline2rv(l1, l2)
    now = datetime.utcnow()
    coords = []

    for i in range(steps):
        t = now + timedelta(minutes=i)
        jd, fr = jday(t.year, t.month, t.day, t.hour, t.minute, t.second)
        e, r, v = sat.sgp4(jd, fr)
        if e == 0:
            coords.append(r)

    return np.array(coords) if coords else np.zeros((0,3))

# -----------------------------
# 4) ML: Anomaly Detection
# -----------------------------
def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.assign(anomaly=[])
    X = df[['velocity_kmph']].values
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X)
    df = df.copy()
    df['anomaly'] = model.predict(X)  # -1 anomaly, 1 normal
    return df

# -----------------------------
# LOAD DATA
# -----------------------------
if not NASA_API_KEY:
    st.error("NASA_API_KEY not found. Set it in .env or environment variables.")
    st.stop()

asteroids = get_asteroids(NASA_API_KEY)
asteroids = detect_anomalies(asteroids)
sats = get_tle(num_sats)

# -----------------------------
# UI: ASTEROIDS TABLE
# -----------------------------
st.subheader("🌍 Asteroid Feed (from NASA)")
st.dataframe(asteroids.head(20), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.metric("Total asteroids (today window)", int(len(asteroids)))
with col2:
    st.metric("Flagged anomalies (ML)", int((asteroids['anomaly'] == -1).sum()))

# -----------------------------
# 3D VISUALIZATION
# -----------------------------
st.subheader("🛰️ 3D Orbit Visualization (Near-Earth Space)")

fig = go.Figure()

# Plot satellite orbits
for name, l1, l2 in sats:
    coords = propagate(l1, l2, steps=steps)
    if coords.shape[0] == 0:
        continue
    fig.add_trace(go.Scatter3d(
        x=coords[:, 0],
        y=coords[:, 1],
        z=coords[:, 2],
        mode='lines',
        name=name
    ))

# Earth sphere (radius ~6371 km)
u, v = np.mgrid[0:2*np.pi:60j, 0:np.pi:30j]
x = 6371 * np.cos(u) * np.sin(v)
y = 6371 * np.sin(u) * np.sin(v)
z = 6371 * np.cos(v)

fig.add_trace(go.Surface(
    x=x, y=y, z=z,
    opacity=0.25,
    showscale=False
))

fig.update_layout(
    scene=dict(
        xaxis_title='X (km)',
        yaxis_title='Y (km)',
        zaxis_title='Z (km)'
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=700
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# “REAL-TIME” AUTO-REFRESH LOOP
# -----------------------------
placeholder = st.empty()
with placeholder.container():
    st.caption(f"Auto-refreshing every {refresh_sec}s (simulated near-real-time)")

# Simple loop trigger
# NOTE: Streamlit reruns the script; we use a sleep to create periodic refresh.
time.sleep(refresh_sec)
st.experimental_rerun()
