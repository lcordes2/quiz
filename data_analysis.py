import pandas as pd
import numpy as np
from collections import Counter
import streamlit as st

SHEET_ID = "13Vj450UMswqv0ycWIg3ZMTW42QNdYNDJpkAEKTvrh5Y"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"



@st.cache_data(ttl=3600) # Data is only cached for max of 1 hour, to receive new entries
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