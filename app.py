import streamlit as st
import data_analysis as da
import altair as alt


actually_tab, teams_tab = st.tabs(["Team Statistics", "Team Comparisons"])
actually_full_df, teams_full_df, players = da.load_data()



### Filter sidebar ###

with st.sidebar:
    st.title("Filters")
    date_min, date_max = actually_full_df["Date"].min(), actually_full_df["Date"].max()

    # if st.button("Clear all filters"):
    #     pass
        

    st.header("Date")
    earliest_date = st.date_input(
        "Include games starting from",
        min_value= date_min,
        max_value=date_max,
        value=(date_min) 
    )
    latest_date = st.date_input(
        "Include games until",
        min_value= date_min,
        max_value=date_max,
        value=(date_max) 
    )

    filter_player = st.selectbox("Only include games featuring", options=["All"] + players)


    actually_df = da.apply_filter(
        actually_full_df, 
        date_range=[earliest_date, latest_date],
        player=filter_player,
    )


### Only AIFP stats ###
with actually_tab:
    st.title("Actually in First Place Statistics 2023")
    if actually_df.shape[0] > 0: # Only show plots if filter includes at least one game

        n_games, first_date, last_date = da.get_games_range(actually_df)
        st.write(f"Based on {n_games} games from {first_date} to {last_date}")

        col1, _, col2 = st.columns([10, 1, 10])

        with col1:
            # Line plot: Points over time (Maybe show average toeter and winner line as well)
            title = alt.TitleParams("Final scores over time", anchor="middle")
            y_min = actually_df["Points"].min() - 5
            y_max = actually_df["Points"].max() + 5
            date_chart =alt.Chart(actually_df, title=title).mark_line(clip=True, point=True).encode(
                alt.X('Date:T'),
                alt.Y('Points:Q', scale=alt.Scale(domain=[y_min, y_max]), title="Score")
            )
            st.altair_chart(date_chart, use_container_width=True)

            # Bar plot: Average points per round 
            round_dat = da.get_average_per_round(actually_df)
            title = alt.TitleParams("Average scores per round", anchor="middle")
            y_min = round_dat["Average score"].min() - 0.5
            y_max = round_dat["Average score"].max() + 0.5
            round_chart = alt.Chart(round_dat, title=title).mark_bar(clip=True).encode(
                alt.X('Rounds:N'),
                alt.Y('Average score:Q', scale=alt.Scale(domain=[y_min, y_max]))
            )
            st.altair_chart(round_chart, use_container_width=True)
            

        with col2:
            # Bar plot: Number of games per player (convert to stack barplots for Wednesday and Sunday
            player_dat = da.get_games_per_player(actually_df)
            title = alt.TitleParams("Number of Games per Player", anchor="middle")
            games_per_player_chart = alt.Chart(player_dat, title=title).mark_bar().encode(
                alt.X('Players:N', sort='-y'),
                alt.Y('Games played:Q')
            )
            st.altair_chart(games_per_player_chart, use_container_width=True)

            # Density plot: Point distribution (show wednesday and sunday as different distribution)
            title = alt.TitleParams("Distribution of final scores", anchor="middle")
            density_chart = alt.Chart(actually_df, title=title).transform_density(
                'Points',
                as_=['Scores', 'Density'],
                groupby=["Weekday"],
                extent=[50, 80]
            ).mark_area().encode(
                x="Scores:Q",
                y= alt.Y('Density:Q', axis=alt.Axis(labels=False, title=None)),
                color='Weekday:N',
            ).configure_legend(
            orient='bottom',
            title=None,
            )
            st.altair_chart(density_chart, use_container_width=True)
    
    else:
        st.write("No games found for the current filter")

### Stats with other teams ###
with teams_tab:
    st.header("Coming soon")
