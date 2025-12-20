import streamlit as st
import pandas as pd

st.title("🔧 Pit Stops Analysis")

st.info(
    "Pit stop data is only available from the 2011 season onward. "
    "Earlier seasons do not have recorded pit stop information."
)

@st.cache_data
def load_data():
    races = pd.read_csv("data/races.csv", usecols=["raceId", "year", "name"])
    pit_stops = pd.read_csv("data/pit_stops.csv", usecols=["raceId", "driverId", "milliseconds"])
    drivers = pd.read_csv("data/drivers.csv", usecols=["driverId", "forename", "surname"])
    return races, pit_stops, drivers

races, pit_stops, drivers = load_data()

season = st.selectbox(
    "Select Season",
    sorted(races[races["year"] >= 2011]["year"].unique())
)

season_races = races[races["year"] == season]

race = st.selectbox("Select Race", season_races["name"])

race_id = season_races[season_races["name"] == race]["raceId"].iloc[0]

race_pits = pit_stops[pit_stops["raceId"] == race_id]

if race_pits.empty:
    st.warning("No pit stop data for this race.")
    st.stop()

summary = (
    race_pits
    .groupby("driverId", as_index=False)
    .agg(
        Pit_Stops=("milliseconds", "count"),
        Avg_Pit_Time_ms=("milliseconds", "mean")
    )
    .merge(drivers, on="driverId")
)

summary["Driver"] = summary["forename"] + " " + summary["surname"]
summary["Avg_Pit_Time_sec"] = summary["Avg_Pit_Time_ms"] / 1000

st.dataframe(
    summary[["Driver", "Pit_Stops", "Avg_Pit_Time_sec"]]
    .sort_values("Avg_Pit_Time_sec"),
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    summary.set_index("Driver")["Avg_Pit_Time_sec"]
)
