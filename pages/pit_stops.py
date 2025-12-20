import streamlit as st
import pandas as pd

st.title("🔧 Pit Stops Analysis")

st.info(
    "ℹ️ Pit stop data is only available from the 2011 season onward. "
    "Earlier seasons do not have recorded pit stop information."
)

@st.cache_data
def load_data():
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
    races, pit_stops, drivers = load_data()

# Only seasons with pit stop data
available_years = sorted(races[races["year"] >= 2011]["year"].unique())

season = st.selectbox(
    "Select Season",
    available_years
)

races_season = races[races["year"] == season]

race_name = st.selectbox(
    "Select Race",
    races_season["name"]
)

race_id = races_season[
    races_season["name"] == race_name
]["raceId"].iloc[0]

pit_race = pit_stops[pit_stops["raceId"] == race_id]

if pit_race.empty:
    st.warning("No pit stop data available for this race.")
    st.stop()

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

st.subheader(f"Pit Stops — {race_name} ({season})")

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
