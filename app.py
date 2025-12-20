import streamlit as st

st.set_page_config(page_title="F1 Dashboard", layout="wide")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Season Leaderboard", "Pit Stops Analysis"]
)

if page == "Season Leaderboard":
    import pages.season_leaderboard
else:
    import pages.pit_stops
