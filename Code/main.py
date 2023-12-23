import pandas as pd

from MySQL_connection import get_sql_data
 
""" ------------------------------------------------------------------------------------------------- """

def clean_artist_name(rankings_df: pd.DataFrame):
    rankings_df["artist"] = rankings_df["artist"].str.split(",")
    artist_list = []
    for i in range(len(rankings_df)):
        for artist in rankings_df.loc[i, "artist"]:
            artist_list.append([i, artist])
    return pd.DataFrame(artist_list, columns=["index", "artist"])

print(clean_artist_name(get_sql_data("weekly_rankings")))