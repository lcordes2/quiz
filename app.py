import streamlit as st
import data_analysis as da
from actually_tab import actually_tab
from top_ten_tab import top_ten_tab

st.elements.utils._shown_default_value_warning = True

# Setup tabs and load data
teams_tab, team_tab = st.tabs(["Top Ten", "Actually in First Place"])
actually_full_df, top_ten_df, players = da.load_data()

### Actually stats ###
with team_tab:
    actually_tab(actually_full_df, players)

### Stats with other teams ###
with teams_tab:
    top_ten_tab(top_ten_df)
