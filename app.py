import streamlit as st
import pandas as pd

st.set_page_config(page_title="F1 Dashboard", layout="wide")
st.title("🏆 Formula 1 — Season Leaderboard")

@st.cache_data
def load_data():
    races = pd.read_csv("data/races.csv", usecols=["raceId", "year"])
    results = pd.read_csv("data/results.csv", usecols=["raceId", "driverId", "points"])
    drivers = pd.read_csv("data/drivers.csv", usecols=["driverId", "forename", "surname"])
    return races, results, drivers

races, results, drivers = load_data()

season = st.selectbox("Select Season", sorted(races["year"].unique()))

races_season = races[races["year"] == season]

season_results = results.merge(races_season, on="raceId")

standings = (
    season_results
    .groupby("driverId", as_index=False)
    .agg(Total_Points=("points", "sum"))
    .merge(drivers, on="driverId")
    .sort_values("Total_Points", ascending=False)
)

standings["Driver"] = standings["forename"] + " " + standings["surname"]

st.dataframe(
    standings[["Driver", "Total_Points"]],
    use_container_width=True,
    hide_index=True
)
