import streamlit as st
import pandas as pd

st.title("🏆 Formula 1 — Season Leaderboard")

@st.cache_data
def load_data():
    races = pd.read_csv(
        "data/races.csv",
        usecols=["raceId", "year", "name"]
    )

    results = pd.read_csv(
        "data/results.csv",
        usecols=["raceId", "driverId", "points"]
    )

    drivers = pd.read_csv(
        "data/drivers.csv",
        usecols=["driverId", "forename", "surname"]
    )

    return races, results, drivers


with st.spinner("Loading season data..."):
    races, results, drivers = load_data()

season = st.selectbox(
    "Select Season",
    sorted(races["year"].unique())
)

races_season = races[races["year"] == season]

season_results = results.merge(
    races_season[["raceId"]],
    on="raceId",
    how="inner"
)

standings = (
    season_results
    .groupby("driverId", as_index=False)
    .agg(
        Total_Points=("points", "sum"),
        Races=("raceId", "count")
    )
    .merge(drivers, on="driverId", how="left")
    .sort_values("Total_Points", ascending=False)
)

standings["Driver"] = (
    standings["forename"] + " " + standings["surname"]
)

st.subheader(f"Season Standings — {season}")

st.dataframe(
    standings[["Driver", "Total_Points", "Races"]],
    use_container_width=True,
    hide_index=True
)

