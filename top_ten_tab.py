import streamlit as st
import pandas as pd
import data_analysis as da
import altair as alt
import utilities

def top_ten_tab(top_ten_df):
    st.title("Top Ten Teams Statistics 2023")
    index = top_ten_df["Team Name"].unique()
    mean_score = top_ten_df.groupby("Team Name")["Points"].mean().round(2)
    total_score = top_ten_df.groupby("Team Name")["Points"].sum()
    mean_rank = top_ten_df.groupby("Team Name")["Rank"].mean().round()
    n_games = top_ten_df[   "Team Name"].value_counts()

    summary_df = pd.DataFrame(index=index, 
        data={
            "Total score": total_score,
            "Average score": mean_score,
            "Average Rank": mean_rank,
            "Games played": n_games
        }
    )
    summary_df = summary_df.sort_values("Total score", ascending=False)
    st.write(summary_df)
 
    ### Plots ###
    # title = alt.TitleParams("Final scores over time", anchor="middle")
    # y_min = actually_df["Points"].min() - 5
    # y_max = actually_df["Points"].max() + 5
    # date_chart =alt.Chart(actually_df, title=title).mark_line(clip=True, point=True).encode(
    #     alt.X('Date:T'),
    #     alt.Y('Points:Q', scale=alt.Scale(domain=[y_min, y_max]), title="Score")
    # )
    # st.altair_chart(date_chart, use_container_width=True)