import streamlit as st

st.set_page_config(page_title="F1 Dashboard", layout="wide")

st.title("🏎️ Formula 1 Dashboard")

st.sidebar.header("Filters")
st.sidebar.selectbox("Season", [2022, 2023, 2024])
st.sidebar.selectbox("Race", ["Bahrain GP", "Monaco GP", "British GP"])

st.success("UI loaded successfully")
