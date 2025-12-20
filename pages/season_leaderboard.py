import streamlit as st
import pandas as pd

def render():
    st.header("🏆 Formula 1 — Leaderboards")

    # =========================
    # Load data
    # =========================
    @st.cache_data
    def load_data():
        races = pd.read_csv(
            "data/races.csv",
            usecols=["raceId", "year", "name"]
        )

        results = pd.read_csv(
            "data/results.csv",
            usecols=["raceId", "driverId", "points", "positionOrder", "grid", "laps"]
        )

        drivers = pd.read_csv(
            "data/drivers.csv",
            usecols=["driverId", "forename", "surname"]
        )

        return races, results, drivers

    races, results, drivers = load_data()

    # =========================
    # Controls
    # =========================
    season = st.selectbox(
        "Select Season",
        sorted(races["year"].unique())
    )

    leaderboard_type = st.radio(
        "Leaderboard Type",
        ["Season Standings", "Race Leaderboard"],
        horizontal=True
    )

    races_season = races[races["year"] == season]

    # =========================
    # SEASON LEADERBOARD
    # =========================
    if leaderboard_type == "Season Standings":
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

        st.subheader(f"🏆 Season Standings — {season}")

        st.dataframe(
            standings[["Driver", "Total_Points", "Races"]],
            use_container_width=True,
            hide_index=True
        )

    # =========================
    # RACE LEADERBOARD
    # =========================
    else:
        race_name = st.selectbox(
            "Select Race",
            races_season["name"]
        )

        race_id = races_season[
            races_season["name"] == race_name
        ]["raceId"].iloc[0]

        race_results = (
            results[results["raceId"] == race_id]
            .merge(drivers, on="driverId", how="left")
            .sort_values("positionOrder")
        )

        race_results["Driver"] = (
            race_results["forename"] + " " + race_results["surname"]
        )

        st.subheader(f"🏁 {race_name} ({season}) — Race Leaderboard")

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
