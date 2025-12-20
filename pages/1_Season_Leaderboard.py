import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("🏆 Season & Race Leaderboards")

@st.cache_data
def load_data():
    races = pd.read_csv("data/races.csv")
    results = pd.read_csv("data/results.csv")
    drivers = pd.read_csv("data/drivers.csv")
    circuits = pd.read_csv("data/circuits.csv")
    return races, results, drivers, circuits

races, results, drivers, circuits = load_data()

years = sorted(races["year"].unique())
season = st.selectbox("Select Season", years, index=len(years)-1)

races_season = races[races["year"] == season]

mode = st.radio("Leaderboard Type", ["Season Standings", "Race Leaderboard"])

if mode == "Season Standings":
    df = (
        results.merge(races_season, on="raceId")
        .merge(drivers, on="driverId")
        .groupby(["forename", "surname"], as_index=False)["points"]
        .sum()
        .sort_values("points", ascending=False)
    )
    df["Driver"] = df["forename"] + " " + df["surname"]
    st.dataframe(df[["Driver", "points"]].rename(columns={"points": "Total Points"}))

else:
    race_name = st.selectbox("Select Race", races_season["name"].tolist())
    race_id = races_season[races_season["name"] == race_name]["raceId"].iloc[0]

    df = (
        results[results["raceId"] == race_id]
        .merge(drivers, on="driverId")
        .sort_values("positionOrder")
    )
    df["Driver"] = df["forename"] + " " + df["surname"]

    st.dataframe(
        df[["positionOrder", "Driver", "grid", "points", "laps"]]
        .rename(columns={"positionOrder": "Position"})
    )
