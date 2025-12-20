import streamlit as st
import pandas as pd
import pydeck as pdk


def render():
    st.header("🏆 Formula 1 — Leaderboards")

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

    leaderboard_type = st.radio(
        "Leaderboard Type",
        ["Season Standings", "Race Leaderboard"],
        horizontal=True
    )

    races_season = races[races["year"] == season]

    # =========================
    # SEASON STANDINGS
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
    # RACE LEADERBOARD (MAP + DROPDOWN)
    # =========================
    else:
        # Merge races with circuit locations
        races_map = (
            races_season
            .merge(circuits, on="circuitId", how="left", suffixes=("_race", "_circuit"))
            .dropna(subset=["lat", "lng"])
        )

        # ---- Dropdown selector (race names)
        st.subheader("🏁 Select Race")

        dropdown_race = st.selectbox(
            "Race (dropdown)",
            races_map["name_race"].tolist(),
            index=0
        )

        # ---- World map selector
        st.subheader("🌍 Or click a race on the map")

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=races_map,
            get_position=["lng", "lat"],
            get_radius=120000,
            get_fill_color=[200, 30, 0, 160],
            pickable=True,
        )

        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=pdk.ViewState(
                latitude=20,
                longitude=0,
                zoom=1.2,
            ),
            tooltip={
                "text": "{name_race}\n{name_circuit}, {country}"
            },
        )

# ---- Dropdown selector (single source of truth)
st.subheader("🏁 Select Race")

selected_race_name = st.selectbox(
    "Race",
    races_map["name_race"].tolist(),
    index=0
)

selected_race_id = races_map[
    races_map["name_race"] == selected_race_name
]["raceId"].iloc[0]


        selected_race_id = races_map[
            races_map["name_race"] == selected_race_name
        ]["raceId"].iloc[0]

        # ---- Leaderboard
        race_results = (
            results[results["raceId"] == selected_race_id]
            .merge(drivers, on="driverId", how="left")
            .sort_values("positionOrder")
        )

        race_results["Driver"] = (
            race_results["forename"] + " " + race_results["surname"]
        )

        st.subheader(f"🏁 {selected_race_name} ({season}) — Race Leaderboard")

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
