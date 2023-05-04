import streamlit as st

def update_filter(df):
    st.session_state["player_select"] = "All Players"
    st.session_state["date_range"] = (
        df["Date"].min().strftime("%d/%m/%y"),
        df["Date"].max().strftime("%d/%m/%y")
    )

def empty_space():
    st.markdown("#")