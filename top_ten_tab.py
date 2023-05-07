import streamlit as st
import pandas as pd
import data_analysis as da
import altair as alt
import utilities

def top_ten_tab(top_ten_df):

    summary_df, team_names = da.get_top_ten_summary(top_ten_df)
    st.write(summary_df)
 
    utilities.empty_space()
    st.header("Team comparisons")

    selected_teams = st.multiselect("Select teams to include", options=team_names, default=["Actually in First Place", "Team Wasmachien"])
    select_df = top_ten_df.loc[top_ten_df["Team Name"].isin(selected_teams)]


    if len(selected_teams) > 0:
    ### Plots ###

        # Line plot: Final scores over time
        title = alt.TitleParams("Final scores over time", anchor="middle")
        y_min = select_df["Points"].min() - 5
        y_max = select_df["Points"].max() + 5
        date_chart =alt.Chart(select_df, title=title).mark_line(clip=True, point=True).encode(
            alt.X('Date:T'),
            alt.Y('Points:Q', scale=alt.Scale(domain=[y_min, y_max]), title="Score"),
            color='Team Name:N'
        )
        st.altair_chart(date_chart, use_container_width=True)

        utilities.empty_space()


        # Bar plot: Ranks 
        rank_counts = da.get_rank_distribution(select_df)
        title = alt.TitleParams("Number of times each top ten position was achieved", anchor="middle")        # y_min = round_dat["Average score"].min() - 0.5
        print(rank_counts)
        rank_chart = alt.Chart(rank_counts, title=title).mark_bar().encode(
            alt.X('Rank:O', axis=alt.Axis(labels=True, title='Top ten position', labelAngle=0)),
            alt.Y('Count:Q', axis=alt.Axis(tickMinStep=1)),
            color="Team Name:N",
            column= "Team Name:N"
        ).configure_legend(
        title=None,
        )

        st.altair_chart(rank_chart)

    else:
        st.write("Please select at least one team")