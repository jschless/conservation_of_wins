import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_yearly_url(year):
    return f"https://www.nfl.com/standings/league/{year}/REG"

dfs = []
for year in range(1922, 2022):
    page = requests.get(get_yearly_url(year))
    soup = BeautifulSoup(page.content, "html.parser")
    df = pd.read_html(str(soup.find("table")))[0]
    df["year"] = year 
    dfs.append(df)

dataset = pd.concat(dfs)
dataset.to_csv("nfl_data.csv")
