import streamlit as st
import pages.season_leaderboard as season
import pages.pit_stops as pits

st.set_page_config(page_title="F1 Dashboard", layout="wide")

st.title("🏎️ Formula 1 Dashboard")

page = st.radio(
    "Choose page",
    ["Season Leaderboard", "Pit Stops Analysis"],
    horizontal=True
)

if page == "Season Leaderboard":
    season.render()
else:
    pits.render()
