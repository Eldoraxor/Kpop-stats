import pandas as pd
import requests
from bs4 import BeautifulSoup

from MySQL_connection import get_sql_data

#Function that returns all the kpop artists stored in dbkpop.com
def get_artists():
    columns = ["Link", "Profile", "Stage name", "Full name", "Korean name", 
            "Korean stage name", "Date of birth", "Group", "Country", 
            "Second country", "Height", "Weight", "Bithplace", "Other group", 
            "Former group", "Gender", "Position", "Instagram", "Twitter"]
    response = requests.get('https://dbkpop.com/db/all-k-pop-idols/')
    soup = BeautifulSoup(response.text, 'lxml')
    tbody = soup.find("tbody")

    artists = []
    for line in tbody.find_all("tr"):
        try :
            group = [line.find("td").find("a", href=True)['href']]
        except:
            group = [""]
        artists.append(group + [column.text for column in line.find_all("td")])
    artists_df = pd.DataFrame(artists, columns=columns)

    return artists_df

def clean_artist_name(rankings_df: pd.DataFrame):
    rankings_df["artist"] = rankings_df["artist"].str.split(",")
    artist_list = []
    for i in range(len(rankings_df)):
        for artist in rankings_df.loc[i, "artist"]:
            artist_list.append([i, artist])
    return pd.DataFrame(artist_list, columns=["index", "artist"])

def get_artist_id():
    artists_df = get_sql_data("artists")
    artist_ranking_df = get_sql_data("artist_weekly_ranking")
    artist_id = []
    for artist in artist_ranking_df["artist"]:
        artist_id.append(list(artists_df[artists_df["Korean stage name"].eq(artist)]["index"]))
        if len(list(artists_df[artists_df["Korean stage name"].eq(artist)]["index"]))>1:
            print(artist)
    artist_ranking_df["artist_id"] = artist_id
    return artist_ranking_df

def get_groups():
    columns = ["Link", "Profile", "Name", "Short", "Korean name", 
        "Debut", "Company", "Memebers", "Orig. Memb.", 
        "Fanclub Name", "Active"]
    groups = []
    for group_type in ["girlgroups", "boybands"]:
        response = requests.get(f'https://dbkpop.com/db/k-pop-{group_type}/')
        soup = BeautifulSoup(response.text, 'lxml')
        tbody = soup.find("tbody")

        for line in tbody.find_all("tr"):
            try :
                group = [line.find("td").find("a", href=True)['href']]
            except:
                group = [""]
            groups.append(group + [column.text for column in line.find_all("td")])
    groups_df = pd.DataFrame(groups, columns=columns)
    return groups_df

print(get_groups())