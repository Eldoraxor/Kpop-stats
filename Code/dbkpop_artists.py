import pandas as pd
import requests
from bs4 import BeautifulSoup

from MySQL_connection import register_data, get_sql_data

#Function that returns all the kpop artists stored in dbkpop.com
def get_artists_infos():
    columns = ["Profile", "Stage name", "Full name", "Korean name", 
            "Korean stage name", "Date of birth", "Group", "Country", 
            "Second country", "Height", "Weight", "Bithplace", "Other group", 
            "Former group", "Gender", "Position", "Instagram", "Twitter"]
    response = requests.get('https://dbkpop.com/db/all-k-pop-idols/')
    soup = BeautifulSoup(response.text, 'lxml')
    tbody = soup.find("tbody")

    artists = []
    for line in tbody.find_all("tr"):
        artists.append([column.text for column in line.find_all("td")])
    artists_df = pd.DataFrame(artists, columns=columns)

    return artists_df

def get_artist_id():
    artists_df = get_sql_data("artists")
    artist_ranking_df = get_sql_data("artist_weekly_ranking")
    artist_id = []
    for artist in artist_ranking_df["artist"]:
        artist_id.append(list(artists_df[artists_df["Korean stage name"].eq(artist)]["artists_id"]))
        if len(list(artists_df[artists_df["Korean stage name"].eq(artist)]["artists_id"]))>1:
            print(artist)
    artist_ranking_df["artist_id"] = artist_id