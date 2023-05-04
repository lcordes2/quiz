import streamlit as st
import data_analysis as da
from actually_tab import actually_tab
from all_teams_tab import all_teams_tab

st.elements.utils._shown_default_value_warning = True

# Setup tabs and load data
team_tab, teams_tab = st.tabs(["Team Statistics", "Team Comparisons"])
actually_full_df, teams_full_df, players = da.load_data()

### Actually stats ###
with team_tab:
    actually_tab(actually_full_df, players)

### Stats with other teams ###
with teams_tab:
    all_teams_tab(teams_full_df)
