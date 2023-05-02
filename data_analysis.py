import pandas as pd


SHEET_ID = "13Vj450UMswqv0ycWIg3ZMTW42QNdYNDJpkAEKTvrh5Y"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"



def get_data():
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

s

ubset = actually_df.filter(regex="^Player\d$")
subset.squeeze(axis=0)
print(subset)

actually_df["Points"].plot.density()
#actually_df.plot.line(x="Date", y="Points")


print(actually_df[actually_df["Weekday"]=="Wednesday"]["Points"].mean())
print(actually_df[actually_df["Weekday"]=="Sunday"]["Points"].mean())
