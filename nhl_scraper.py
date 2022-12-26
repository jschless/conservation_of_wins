import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_yearly_url(year):
    return f"https://www.hockey-reference.com/leagues/NHL_{year}_standings.html"

dfs = []
for year in tqdm(range(1950, 2022)):
    if year != 2005: # lockout meant no season
        print(year)
        soup = BeautifulSoup(open(f"./nhl_files/NHL_{year}_standings.html", "r"), "html.parser")
        df = pd.read_html(str(soup.find("table", id="expanded_standings")))[0]
        df["year"] = year 
        dfs.append(df)

dataset = pd.concat(dfs)
dataset.to_csv("nhl_data.csv")

def fetch_all_html_files():
    import subprocess
    import time 
    for year in tqdm(range(1950, 2022)):
        subprocess.call(["wget", get_yearly_url(year)])
        time.sleep(4)