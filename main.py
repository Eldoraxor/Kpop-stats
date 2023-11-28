import pandas as pd
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup

from MySQL_connection import register_data
from MySQL_connection import get_sql_data
 
def get_artists() -> list:
    ranking_df = get_sql_data("ranking")
    artists = list(ranking_df["artist"].unique())
    artists_modified = []
    for artist in artists:
        artists_modified += artist.split(",")
    return artists_modified

""" ------------------------------------------------------------------------------------------------- """

def clean_artist_name(rankings_df: pd.DataFrame):
    rankings_df["artist"] = rankings_df["artist"].str.split(",")
    artist_list = []
    for i in range(len(rankings_df)):
        for artist in rankings_df.loc[i, "artist"]:
            artist_list.append([i, artist])
    return pd.DataFrame(artist_list, columns=["index", "artist"])