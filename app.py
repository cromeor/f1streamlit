import streamlit as st

st.set_page_config(page_title="F1 Dashboard", layout="wide")

st.title("🏎️ Formula 1 Dashboard")
st.write("If you don’t see the sidebar, use these links:")

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_Season_Leaderboard.py", label="🏆 Season & Race Leaderboards")
with col2:
    st.page_link("pages/2_Pit_Stops.py", label="🔧 Pit Stop Analysis (2011+)")

st.divider()
st.caption("Tip: Expand the sidebar using the top-left arrow / menu icon.")
