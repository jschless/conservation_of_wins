import pandas as pd
import numpy as np

from constants import nba_teams, city_list, place_to_area


def extract_city(s):
    for c in city_list:
        if c in s:
            return c


def process_nfl():
    df = pd.read_csv("nfl_data.csv")
    df = df.rename(columns={"NFL Team": "team_name", "PCT": "win_pct"})
    df["sport"] = "nfl"
    teams = open("nfl_teams.txt", "r").read().split("\n")

    def find_matching_team(x):
        for t in teams:
            if all([c in x for c in t]):
                return t
        return x

    df["team_name"] = df["team_name"].apply(find_matching_team)

    return df


def process_mlb():
    df = pd.read_csv("mlb_data.csv")
    df["win_pct"] = df.wins / (df.wins + df.losses)
    df["sport"] = "mlb"
    return df


def process_nba():
    df = pd.read_csv("nba_data.csv")
    df = df.rename(columns={"Winning Percentage": "win_pct"})

    def rename_team(team):
        for t in nba_teams:
            if team in t:
                return t
        print("error with team", team)

    df["team_name"] = df.Team.apply(rename_team)
    df["sport"] = "nba"
    df["year"] = df.Year.apply(lambda x: int(x[:4]))
    return df


def process_nhl():
    df = pd.read_csv("nhl_data.csv")
    df = df.rename(columns={"Unnamed: 1": "team_name"})

    def get_win_pct(s):
        w_l_t = s.split("-")
        w, l, t = w_l_t[0], w_l_t[1], w_l_t[2]
        return int(w) / (int(w) + int(t) + int(l))

    df["win_pct"] = df.Overall.apply(get_win_pct)
    df["team_name"] = df.team_name.apply(
        lambda x: "Chicago Blackhawks" if x == "Chicago Black Hawks" else x
    )
    df["sport"] = "nhl"
    return df


def preprocess():
    nfl_df = process_nfl()
    mlb_df = process_mlb()
    nba_df = process_nba()
    nhl_df = process_nhl()
    df_list = [nfl_df, mlb_df, nba_df, nhl_df]

    for df in df_list:
        df["place"] = df.team_name.apply(extract_city)
        df["area"] = df["place"].apply(lambda x: place_to_area.get(x, np.nan))

    cols = ["win_pct", "place", "sport", "team_name", "area", "year"]
    df = pd.concat(df_list)[cols]

    df["sport"] = df["sport"].apply(lambda x: x.upper())
    teams_per_year = (
        df.groupby(["year", "place"])
        .team_name.apply(lambda x: len(x.unique()))
        .reset_index()
    )
    teams_per_year["n_teams"] = teams_per_year["team_name"]
    teams_per_year = teams_per_year.drop(columns=["team_name"])
    df = df.merge(teams_per_year, on=["year", "place"])
    return df
