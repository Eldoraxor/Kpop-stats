from datetime import date
from CircleChart_export import new_rankings, get_kpop_rankings
from MySQL_connection import register_data, get_sql_data
from dbkpop_export import get_artists, clean_artist_name, get_groups

#Function that updates the data for "weekly_ranking", "artists" and "artist_weekly_ranking"
#Updated data retrieved with new_rankings(), get_artists_infos() and get_artist_id()
def update():
    register_data(new_rankings(), "weekly_rankings", method="append")
    register_data(get_artists(), "artists", "replace")
    register_data(get_groups(), "groups", "replace")
    register_data(clean_artist_name(get_sql_data("weekly_rankings")), "artist_weekly_ranking", "replace")

#Function that reloads the ranking data
# !! TO BE USED ONLY WHEN MISSMANIPULATION 
def reload():
    rankings_df = get_kpop_rankings("weekly", date(2010,1,1), date.today())
    register_data(rankings_df, "weekly_ranking", method="replace")

update()