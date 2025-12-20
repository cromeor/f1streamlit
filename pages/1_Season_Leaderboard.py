import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide")
st.header("🏆 Formula 1 — Season & Race Leaderboards")

# =========================
# Load data
# =========================
@st.cache_data
def load_data():
    races = pd.read_csv(
        "data/races.csv",
        usecols=["raceId", "year", "name", "circuitId"]
    )
    circuits = pd.read_csv(
        "data/circuits.csv",
        usecols=["circuitId", "name", "location", "country", "lat", "lng"]
    )
    results = pd.read_csv(
        "data/results.csv",
        usecols=["raceId", "driverId", "points", "positionOrder", "grid", "laps"]
    )
    drivers = pd.read_csv(
        "data/drivers.csv",
        usecols=["driverId", "forename", "surname"]
    )
    return races, circuits, results, drivers

races, circuits, results, drivers = load_data()

# =========================
# Controls
# =========================
season = st.selectbox(
    "Select Season",
    sorted(races["year"].unique())
)

mode = st.radio(
    "Leaderboard Type",
    ["Season Standings", "Race Leaderboard"],
    horizontal=True
)

races_season = races[races["year"] == season]

# =========================
# SEASON STANDINGS
# =========================
if mode == "Season Standings":
    standings = (
        results.merge(races_season[["raceId"]], on="raceId")
        .groupby("driverId", as_index=False)
        .agg(Total_Points=("points", "sum"))
        .merge(drivers, on="driverId")
        .sort_values("Total_Points", ascending=False)
    )

    standings["Driver"] = standings["forename"] + " " + standings["surname"]

    st.subheader(f"🏆 Season Standings — {season}")

    st.dataframe(
        standings[["Driver", "Total_Points"]],
        use_container_width=True,
        hide_index=True
    )

# =========================
# RACE LEADERBOARD + MAP
# =========================
else:
    race_name = st.selectbox(
        "Select Race",
        races_season["name"].tolist()
    )

    race_id = races_season[
        races_season["name"] == race_name
    ]["raceId"].iloc[0]

    race_results = (
        results[results["raceId"] == race_id]
        .merge(drivers, on="driverId")
        .sort_values("positionOrder")
    )

    race_results["Driver"] = (
        race_results["forename"] + " " + race_results["surname"]
    )

    st.subheader(f"🏁 {race_name} — {season}")

    st.dataframe(
        race_results[
            ["positionOrder", "Driver", "grid", "points", "laps"]
        ].rename(columns={
            "positionOrder": "Position",
            "grid": "Grid",
            "points": "Points",
            "laps": "Laps"
        }),
        use_container_width=True,
        hide_index=True
    )

    # -------------------------
    # Winner per race
    # -------------------------
    winners = (
        results[results["positionOrder"] == 1]
        .merge(drivers, on="driverId")
        .assign(Winner=lambda d: d["forename"] + " " + d["surname"])
        [["raceId", "Winner"]]
    )

    races_map = (
        races_season
        .merge(circuits, on="circuitId", how="left", suffixes=("_race", "_circuit"))
        .merge(winners, on="raceId", how="left")
        .dropna(subset=["lat", "lng"])
    )
