import streamlit as st


actually_tab, teams_tab = st.tabs(["Team Statistics", "Team Comparisons"])


### Only AIFP stats ###
with actually_tab:
    st.write("Within team stats TEST")



### Stats with other teams ###
with teams_tab:
    st.write("Overall team stats")
