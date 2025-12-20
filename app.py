import streamlit as st

st.set_page_config(page_title="F1 Dashboard", layout="wide")

st.title("🏎️ Formula 1 Dashboard")

col1, col2 = st.columns(2)

with col1:
    if st.button("🏆 Season Leaderboard"):
        st.switch_page("pages/season_leaderboard.py")

with col2:
    if st.button("🔧 Pit Stops Analysis"):
        st.switch_page("pages/pit_stops.py")

st.markdown(
    """
    ### Welcome
    Use the buttons above to navigate between pages.
    """
)
