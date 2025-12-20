import streamlit as st

st.set_page_config(page_title="F1 Dashboard", layout="wide")

st.title("🏎️ Formula 1 Dashboard")

st.sidebar.header("Filters")
st.sidebar.selectbox("Season", [2022, 2023, 2024])
st.sidebar.selectbox("Race", ["Bahrain GP", "Monaco GP", "British GP"])

st.success("UI loaded successfully")

import streamlit as st
import pandas as pd

st.set_page_config(page_title="F1 Dashboard", layout="wide")
st.title("🏎️ Formula 1 Dashboard")

@st.cache_data
def load_races():
    return pd.read_csv(
        "data/races.csv",
        usecols=["raceId", "year", "name"]
    )

with st.spinner("Loading races…"):
    races = load_races()

st.sidebar.header("Filters")

year = st.sidebar.selectbox(
    "Season",
    sorted(races["year"].unique())
)

races_year = races[races["year"] == year]

race = st.sidebar.selectbox(
    "Race",
    races_year["name"]
)

st.success("Races loaded successfully")
