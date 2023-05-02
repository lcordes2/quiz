import pandas as pd
import numpy as np
from collections import Counter

SHEET_ID = "13Vj450UMswqv0ycWIg3ZMTW42QNdYNDJpkAEKTvrh5Y"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"



def load_data():
    sheets = pd.ExcelFile(URL)
    teams_df = pd.read_excel(sheets, sheet_name="dsFact_Scores")
    actually_df = pd.read_excel(sheets, sheet_name="dsFact_Teamstats")

    actually_df = add_weekday_col(actually_df)
    teams_df = add_weekday_col(teams_df)
    return actually_df, teams_df


def add_weekday_col(df):
    df["Weekday"] = df["Date"].apply(lambda x : x.weekday())
    df["Weekday"] = df["Weekday"].replace([2,6], ["Wednesday", "Sunday"])
    return df


def get_games_range(df):
    return (len(df["Date"]),
        df["Date"].min().strftime('%d/%m/%Y'),
        df["Date"].max().strftime('%d/%m/%Y')
    )

def get_games_per_player(df):
    player_cols = df.filter(regex="^Player\d$")
    game_counts = Counter(player_cols.values.flatten().tolist())
    del game_counts[np.nan]
    return pd.DataFrame({"Players": game_counts.keys(), "Games played": game_counts.values()})


# actually_df["Points"].plot.density()
# actually_df.plot.line(x="Date", y="Points")
# print(actually_df[actually_df["Weekday"]=="Wednesday"]["Points"].mean())
# print(actually_df[actually_df["Weekday"]=="Sunday"]["Points"].mean())
