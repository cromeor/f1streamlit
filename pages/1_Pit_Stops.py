import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pit Stops Analysis", layout="wide")
st.title("🔧 Pit Stops Analysis")

# =========================
# Load data (SAFE)
# =========================
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

# =========================
# Sidebar filters
# =========================
st.sidebar.header("Filters")

season = st.sidebar.selectbox(
    "Select Season",
    sorted(races["year"].unique())
)

races_season = races[races["year"] == season]

race_name = st.sidebar.selectbox(
    "Select Race",
    races_season["name"].values
)

race_id = races_season[
    races_season["name"] == race_name
]["raceId"].iloc[0]

# =========================
# Prepare pit stop stats
# =========================
pit_race = pit_stops[pit_stops["raceId"] == race_id]

pit_summary = (
    pit_race
    .groupby("driverId", as_index=False)
    .agg(
        Avg_Pit_Time_ms=("milliseconds", "mean"),
        Pit_Stops=("milliseconds", "count")
    )
    .merge(drivers, on="driverId", how="left")
)

pit_summary["Driver"] = (
    pit_summary["forename"] + " " + pit_summary["surname"]
)

pit_summary["Avg_Pit_Time_sec"] = (
    pit_summary["Avg_Pit_Time_ms"] / 1000
)

# =========================
# Display table
# =========================
st.subheader(f"📋 Pit Stop Summary — {race_name} ({season})")

table = pit_summary[
    ["Driver", "Pit_Stops", "Avg_Pit_Time_sec"]
].sort_values("Avg_Pit_Time_sec")

st.dataframe(
    table,
    use_container_width=True,
    hide_index=True
)

# =========================
# Charts
# =========================
st.subheader("📊 Average Pit Stop Time per Driver (seconds)")

st.bar_chart(
    data=table.set_index("Driver")["Avg_Pit_Time_sec"]
)
