import pandas as pd
#from Rankings import Circle_rankings
from .context import MySQL

"""config = configparser.ConfigParser()
config.read('config.ini')
connector_dir = {"host" : "localhost",
                 "port" : 3306,
                 "user" : "root",
                 "password" : config["mysql_password"],
                 "database" : "Kpop"}"""

def update_artists():
    last_year  = MySQL.query_mysql("SELECT MAX(year) FROM kpop.weekly_rankings")
    return last_year

print(update_artists)