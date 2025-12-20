import streamlit as st
import pandas as pd

# =========================
# Page config
# =========================
st.set_page_config(page_title="F1 Dashboard", layout="wide")

# =========================
# Sidebar navigation
# =========================
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Season Dashboard", "Pit Stops Analysis"]
)

# =========================
# SEASON DASHBOARD PAGE
# =========================
if page == "Season Dashboard":

    st.title("🏎️ Formula 1 Dashboard")

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

    if track == "All Tracks":
        st.subheader(f"🏆 Season Standings — {season}")

        st.dataframe(
            season_standings[["Driver", "Total_Points", "Races"]],
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

        st.subheader(f"🏁 {track} ({season}) — Race Leaderboard")

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

# =========================
# PIT STOPS PAGE
# =========================
else:

    st.title("🔧 Pit Stops Analysis")

    @st.cache_data
    def load_pit_data():
        races = pd.read_csv(
            "data/races.csv",
            usecols=["raceId", "year", "name"]
        )

        pit_stops = pd.read_csv(
            "data/pit_stops.csv",
            usecols=["raceId", "driverId", "milliseconds"]
        )

        drivers = pd.read_csv(
            "data/drivers.csv",
            usecols=["driverId", "forename", "surname"]
        )

        return races, pit_stops, drivers

    with st.spinner("Loading pit stop data..."):
        races, pit_stops, drivers = load_pit_data()

    st.sidebar.header("Pit Stop Filters")

    season = st.sidebar.selectbox(
        "Select Season",
        sorted(races["year"].unique())
    )

    races_season = races[races["year"] == season]

    race_name = st.sidebar.selectbox(
        "Select Race",
        races_season["name"]
    )

    race_id = races_season[
        races_season["name"] == race_name
    ]["raceId"].iloc[0]

    pit_race = pit_stops[pit_stops["raceId"] == race_id]

    pit_summary = (
        pit_race
        .groupby("driverId", as_index=False)
        .agg(
            Pit_Stops=("milliseconds", "count"),
            Avg_Pit_Time_ms=("milliseconds", "mean")
        )
        .merge(drivers, on="driverId", how="left")
    )

    pit_summary["Driver"] = (
        pit_summary["forename"] + " " + pit_summary["surname"]
    )

    pit_summary["Avg_Pit_Time_sec"] = (
        pit_summary["Avg_Pit_Time_ms"] / 1000
    )

    st.subheader(f"📋 Pit Stops — {race_name} ({season})")

    st.dataframe(
        pit_summary[
            ["Driver", "Pit_Stops", "Avg_Pit_Time_sec"]
        ].sort_values("Avg_Pit_Time_sec"),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("📊 Average Pit Stop Time (seconds)")
    st.bar_chart(
        pit_summary.set_index("Driver")["Avg_Pit_Time_sec"]
    )
