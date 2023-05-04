import streamlit as st
import data_analysis as da
import altair as alt
import utilities


def actually_tab(actually_full_df, players):
    st.title("Actually in First Place Statistics 2023")

    ## Filters ##
    # Set filter defaults
    if "player_select" not in st.session_state or "date_range" not in st.session_state:
        st.session_state["player_select"] = "All Players"
        st.session_state["date_range"] = (
        actually_full_df["Date"].min().strftime("%d/%m/%y"),
        actually_full_df["Date"].max().strftime("%d/%m/%y")
    )

    earliest_date, latest_date = st.select_slider(
        label="Include games between",
        value=st.session_state["date_range"],
        options=actually_full_df["Date"].dt.strftime("%d/%m/%y"),
        key="date_range"
    )  
    filter_player = st.selectbox("Only include games featuring", options=["All Players"] + players, key="player_select")

    actually_df = da.apply_filter(
        actually_full_df, 
        earliest=earliest_date, 
        latest=latest_date,
        player=filter_player,
    )
    n_games = actually_df.shape[0]

    left, right = st.columns([4, 1])
    with left:
        st.write(f"{n_games} game{'' if n_games == 1 else 's'} included")
    with right:
        st.button("Clear filters", on_click=utilities.update_filter, kwargs={"df": actually_full_df})


    utilities.empty_space()

    ## Plots ##
    if n_games > 0: # Only show plots if filter includes at least one game

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
    