import pandas as pd
from datetime import date, timedelta
from Circle_rankings import get_kpop_rankings
from MySQL_connection import query_mysql, register_data

"""config = configparser.ConfigParser()
config.read('config.ini')
connector_dir = {"host" : "localhost",
                 "port" : 3306,
                 "user" : "root",
                 "password" : config["mysql_password"],
                 "database" : "Kpop"}"""

def update_rankings():
    last_year  = query_mysql("SELECT MAX(year) FROM kpop.weekly_ranking")[0][0]
    last_week = query_mysql("SELECT MAX(week) FROM kpop.weekly_ranking WHERE year = " + str(last_year))[0][0]
    
    last_week_date = date.fromisocalendar(last_year, last_week, 1)
    new_week_date = last_week_date + timedelta(weeks=1)

    print(f"Year {last_year} and week {last_week}")
    last_rankings = get_kpop_rankings(by="weekly", date_from=new_week_date, date_until=date.today())
    
    register_data(last_rankings, "weekly_ranking")