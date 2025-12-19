# This code is for DEVELOPMENT ONLY
# You do NOT run Streamlit in Colab

streamlit_code = """
import streamlit as st
import pandas as pd

st.set_page_config(page_title="F1 Dashboard", layout="wide")
st.title("🏎️ Formula 1 Interactive Dashboard")

@st.cache_data
def load_data():
    races = pd.read_csv(
        "data/races.csv",
        usecols=["raceId", "year", "name", "circuitId"]
    )

    results = pd.read_csv(
        "data/results.csv",
        usecols=["raceId", "driverId", "positionOrder", "points", "grid", "laps"]
    )

    drivers = pd.read_csv(
        "data/drivers.csv",
        usecols=["driverId", "forename", "surname"]
    )

    circuits = pd.read_csv(
        "data/circuits.csv",
        usecols=["circuitId", "name", "country"]
    )

    return races, results, drivers, circuits


races, results, drivers, circuits = load_data()
with st.spinner("Loading Formula 1 data..."):
    races, results, drivers, circuits = load_data()

st.sidebar.header("Filters")

year = st.sidebar.selectbox(
    "Select season",
    sorted(races["year"].unique())
)

races_year = races[races["year"] == year]

race_name = st.sidebar.selectbox(
    "Select race",
    races_year["name"].values
)

race = races_year[races_year["name"] == race_name].iloc[0]
race_id = race["raceId"]

circuit = circuits[circuits["circuitId"] == race["circuitId"]].iloc[0]

st.subheader(f"{race_name} ({year})")
st.write(f"📍 Circuit: {circuit['name']} — {circuit['country']}")

race_results = (
    results[results["raceId"] == race_id]
    .merge(drivers, on="driverId", how="left")
    .sort_values("positionOrder")
)

race_results["Driver"] = race_results["forename"] + " " + race_results["surname"]

winner = race_results.iloc[0]
st.success(f"🏆 Winner: {winner['Driver']} ({winner['points']} points)")

st.subheader("🥇 Podium")
st.table(race_results.head(3)[["positionOrder", "Driver", "points"]])

st.subheader("📊 Full Classification")
st.dataframe(
    race_results[["positionOrder", "Driver", "grid", "points", "laps"]],
    use_container_width=True
)
"""
print("Code stored safely. Edit it here.")
