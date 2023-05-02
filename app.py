import streamlit as st
import data_analysis as da
import altair as alt


actually_tab, teams_tab = st.tabs(["Team Statistics", "Team Comparisons"])

### Load data 
actually_df, teams_df = da.load_data()

### Only AIFP stats ###
with actually_tab:
    st.title("Actually in First Place Statistics 2023")
    n_games, first_date, last_date = da.get_games_range(actually_df)
    st.write(f"Based on {n_games} games from {first_date} to {last_date}")

    
    #col1, col2 = st.columns(2)

    #with col1:
    
    # Number of games per player bar chart
    player_dat = da.get_games_per_player(actually_df)
    games_per_player_chart =alt.Chart(player_dat).mark_bar().encode(
        alt.X('Players:N', sort='-y'),
        alt.Y('Games played:Q'))
    st.altair_chart(games_per_player_chart)
    #with col2:
    

### Stats with other teams ###
with teams_tab:
    st.header("Overall team stats")
