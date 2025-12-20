import streamlit as st
import pandas as pd

# =========================
# Page setup
# =========================
st.set_page_config(page_title="F1 Dashboard", layout="wide")
st.title("🏎️ Formula 1 Dashboard")

# =========================
# Load data (SAFE)
# =========================
@st.cache_data
def load_data():
    races = pd.read_csv(
        "data/races.csv",
        usecols=["raceId", "year", "name"]
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

track = st.sidebar.selectbox(
    "Select Track (optional)",
    ["All Tracks"] + sorted(races_season["name"].tolist())
)

# =========================
# SEASON LEADERBOARD
# =========================
season_results = results.merge(
    races_season[["raceId"]],
    on="raceId",
    how="inner"
)

season_standings = (
    season_results
    .groupby("driverId", as_index=False)
    .agg(
        Total_Points=("points", "sum"),
        Races=("raceId", "count")
    )
    .merge(drivers, on="driverId", how="left")
    .sort_values("Total_Points", ascending=False)
)

season_standings["Driver"] = (
    season_standings["forename"] + " " + season_standings["surname"]
)

season_table = season_standings[
    ["Driver", "Total_Points", "Races"]
]

# =========================
# Display logic
# =========================
if track == "All Tracks":
    st.subheader(f"🏆 Season Standings — {season}")

    st.dataframe(
        season_table,
        use_container_width=True,
        hide_index=True
    )

else:
    race_id = races_season[
        races_season["name"] == track
    ]["raceId"].iloc[0]

    race_results = (
        results[results["raceId"] == race_id]
        .merge(drivers, on="driverId", how="left")
        .sort_values("positionOrder")
    )

    race_results["Driver"] = (
        race_results["forename"] + " " + race_results["surname"]
    )

    race_table = race_results[
        ["positionOrder", "Driver", "grid", "points", "laps"]
    ].rename(columns={
        "positionOrder": "Position",
        "grid": "Grid",
        "points": "Points",
        "laps": "Laps"
    })

    st.subheader(f"🏁 {track} ({season}) — Race Leaderboard")

    st.dataframe(
        race_table,
        use_container_width=True,
        hide_index=True
    )
