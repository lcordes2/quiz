import pandas as pd
import numpy as np
from collections import Counter
import streamlit as st

SHEET_ID = "13Vj450UMswqv0ycWIg3ZMTW42QNdYNDJpkAEKTvrh5Y"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"



@st.cache_data(ttl=1800) # Data is only cached for max of 30 min, to receive new entries
def load_data():
    sheets = pd.ExcelFile(URL)
    teams_df = pd.read_excel(sheets, sheet_name="dsFact_Scores")
    top_ten = teams_df.groupby("Team Name")["Points"].sum().sort_values(ascending=False)[0:10]
    teams_df = teams_df.loc[teams_df["Team Name"].isin(top_ten.index)]
    actually_df = pd.read_excel(sheets, sheet_name="dsFact_Teamstats")

    actually_df = add_weekday_col(actually_df)
    teams_df = add_weekday_col(teams_df)
    players = list(get_games_per_player(actually_df)["Players"])
    return actually_df, teams_df, players


def add_weekday_col(df):
    df["Weekday"] = df["Date"].apply(lambda x : x.weekday())
    df["Weekday"] = df["Weekday"].replace([2,6], ["Wednesday", "Sunday"])
    return df


def get_games_per_player(df):
    player_cols = df.filter(regex="^Player\d$")
    game_counts = Counter(player_cols.values.flatten().tolist())
    game_counts_cleaned = {key: game_counts[key] for key in game_counts if isinstance(key, str)} # remove nans
    return pd.DataFrame({"Players": game_counts_cleaned.keys(), "Games played": game_counts_cleaned.values()})

def get_average_per_round(df):  
    round_cols = df.filter(regex="^Score_R\d$")
    round_means = round_cols.mean(axis=0)   
    rounds = [int(r.replace("Score_R", "")) for r in round_means.keys()]
    return pd.DataFrame({"Rounds": rounds, "Average score": np.round(round_means.values, 2)})   

def apply_filter(df, earliest, latest, player):
    # Date filter
    earliest = pd.to_datetime(earliest, format="%d/%m/%y")
    latest = pd.to_datetime(latest, format="%d/%m/%y")
    filtered = df.loc[(df['Date'] >= earliest)
                     & (df['Date'] <= latest)]
    
    # Player filter
    if not player == "All Players":
        filtered = filtered[filtered.isin([player]).any(axis=1)]
    return filtered


def get_top_ten_summary(df):
    st.title("Top Ten Teams Statistics 2023")
    team_names = df["Team Name"].unique()
    mean_score = df.groupby("Team Name")["Points"].mean().round(2)
    total_score = df.groupby("Team Name")["Points"].sum()
    high_score = df.groupby("Team Name")["Points"].max()
    mean_rank = df.groupby("Team Name")["Rank"].mean().round()
    n_games = df["Team Name"].value_counts()

    summary_df = pd.DataFrame(index=team_names, 
        data={
            "Team name": team_names,
            "Total score": total_score,
            "Average score": mean_score,
            "High score": high_score,
            "Average rank": mean_rank,
            "Games played": n_games,
        }
    ).reset_index(drop=True)

    return summary_df.sort_values("Total score", ascending=False), team_names

def get_rank_distribution(df):
    df = df.loc[df["Rank"].isin(range(1, 11))]
    counts = df.groupby("Team Name")["Rank"].value_counts()
    rank_counts = pd.DataFrame({
        "Team Name": counts.index.get_level_values(0),
        "Rank": counts.index.get_level_values(1),
        "Count": list(counts)
    })
    return rank_counts