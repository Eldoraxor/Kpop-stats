from datetime import date
from Circle_rankings import new_rankings, get_kpop_rankings
from MySQL_connection import register_data
from dbkpop_artists import get_artists_infos, get_artist_id

def update():
    new_rankings_df = new_rankings()
    register_data(new_rankings_df, "weekly_ranking", method="append")
    register_data(get_artists_infos(), "artists", "replace")
    register_data(get_artist_id(), "artist_weekly_ranking", "replace")

def reload():
    rankings_df = get_kpop_rankings("weekly", date(2010,1,1), date.today())
    register_data(rankings_df, "weekly_rankings", method="replace")