import streamlit as st
import pandas as pd

# =========================
# Page setup
# =========================
st.set_page_config(page_title="F1 Dashboard", layout="wide")
st.title("🏎️ Formula 1 Leaderboard Dashboard")

# =========================
# Load data (SAFE VERSION)
# =========================
@st.cache_data
def load_data():
    races = pd.read_csv(
        "data/races.csv",
        usecols=["raceId", "year", "name", "circuitId"]
    )

    results = pd.read_csv(
        "data/results.csv",
        usecols=["raceId", "driverId", "positionOrder", "points", "grid", "laps"]
    )

    drivers = pd.read_csv(
        "data/drivers.csv",
        usecols=["driverId", "forename", "surname"]
    )

    return races, results, drivers


with st.spinner("Loading F1 data..."):
    races, results, drivers = load_data()

# =========================
# Sidebar filters
# =========================
st.sidebar.header("Filters")

season = st.sidebar.selectbox(
    "Select Season",
    sorted(races["year"].unique())
)

races_season = races[races["year"] == season]

race_name = st.sidebar.selectbox(
    "Select Race",
    races_season["name"].values
)

# =========================
# Get selected race
# =========================
race_id = races_season[
    races_season["name"] == race_name
]["raceId"].iloc[0]

# =========================
# Build leaderboard
# =========================
leaderboard = (
    results[results["raceId"] == race_id]
    .merge(drivers, on="driverId", how="left")
    .sort_values("positionOrder")
)

leaderboard["Driver"] = (
    leaderboard["forename"] + " " + leaderboard["surname"]
)

leaderboard_display = leaderboard[
    ["positionOrder", "Driver", "grid", "points", "laps"]
].rename(columns={
    "positionOrder": "Position",
    "grid": "Grid",
    "points": "Points",
    "laps": "Laps"
})

# =========================
# Display leaderboard
# =========================
st.subheader(f"🏁 {race_name} ({season}) — Leaderboard")

st.dataframe(
    leaderboard_display,
    use_container_width=True,
    hide_index=True
)
