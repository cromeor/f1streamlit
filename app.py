import streamlit as st

st.set_page_config(
    page_title="F1 Dashboard",
    layout="wide"
)

st.title("🏎️ Formula 1 Dashboard")
st.markdown(
    """
    Use the **sidebar** to navigate between pages.

    - 🏆 Season & Race Leaderboards  
    - 🔧 Pit Stop Analysis (2011+)
    """
)
