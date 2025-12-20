import streamlit as st

st.set_page_config(page_title="F1 Dashboard", layout="wide")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Season Dashboard", "Pit Stops Analysis"]
)

if page == "Season Dashboard":
    import pages.season_dashboard

else:
    import pages.pit_stops
