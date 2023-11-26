import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
from dateutil.relativedelta import relativedelta
import mysql.connector
import configparser
from sqlalchemy import create_engine
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.read('config.ini')
connector_dir = {"host" : "localhost",
                 "port" : 3306,
                 "user" : "root",
                 "password" : "SQLRom3821!",
                 "database" : "Kpop"}

""" Function to register or get data """
def register_data(dataf: pd.DataFrame, table_name: str):
    mydb = mysql.connector.connect(**connector_dir)
    mycursor = mydb.cursor()

    engine = create_engine(f"mysql+mysqlconnector://{connector_dir['user']}:{connector_dir['password']}@{connector_dir['host']}:{connector_dir['port']}/{connector_dir['database']}")
    dataf.to_sql(table_name, con=engine, if_exists='replace', index=True, index_label= f"{table_name}_id")

    mydb.commit()
    mydb.close()

def get_sql_data(table_name: str) -> pd.DataFrame:
    mydb = mysql.connector.connect(**connector_dir)
    mycursor = mydb.cursor()

    engine = create_engine(f"mysql+mysqlconnector://{connector_dir['user']}:{connector_dir['password']}@{connector_dir['host']}:{connector_dir['port']}/{connector_dir['database']}")
    my_df = pd.read_sql_table(table_name, engine)

    mydb.commit()
    mydb.close()

    return my_df
""" -------------------------------- """ 
def get_page_rank_body(driver, period: str, time: int, year: int):
    driver.get("https://circlechart.kr/page_chart/onoff.circle?nationGbn=T&serviceGbn=ALL&targetTime="+str(time)+"&hitYear="+str(year)+"&termGbn="+str(period)+"&yearTime=3")
    return driver.find_element(By.ID, "pc_chart_tbody")

def get_kpop_rankings(by: str, date_from, date_until):
    driver = webdriver.Chrome("D:\Code\Driver\chromedriver-win64\chromedriver.exe")
    songs_rank = []
    for year in range(date_from.year, date_until.year + 1):
        print(f"Year : {year}")
        if by == "monthly":
            period = "month"
            time_max = date_until.month if year == date_until.year else 12
            time_min = date_from.month if year == date_from.year else 1
        elif by == "weekly":
            period = "week"
            time_max = date_until.isocalendar().week if year == date_until.year else date(year, 12, 31).isocalendar().week
            time_min = 1
        print(f"From {time_min} to {time_max}")

        for time in range(time_min,time_max+1):
            print(f"{period} : {time}")
            # USE SELENIUM AS THE SITE USE A JVS TO DISPLAY THE RANKING
            tbody = get_page_rank_body(driver, period, time, year)
            for row in tbody.find_elements(By.TAG_NAME, "tr"):
                rank = row.find_element(By.CLASS_NAME, "text-2xl").text
                song_title = row.find_element(By.CLASS_NAME, "ml-6").find_elements(By.TAG_NAME, "div")[0].text
                artist_and_album = row.find_element(By.CLASS_NAME, "ml-6").find_elements(By.TAG_NAME, "div")[1].text
                #Can try to retrieve label but not working

                data = {
                    "year": year,
                    "time": time,
                    "rank": int(rank),
                    "song_title": song_title,
                    "artist": artist_and_album.split("|")[0].strip(),
                    "album": artist_and_album.split("|")[1].strip()
                }
                if period == "weely":
                    data.rename(columns={"time":"week"})
                elif period == "monthly":
                    data.rename(columns={"time":"month"})
                songs_rank.append(data)
    driver.quit()
    song_ranking_df = pd.DataFrame(songs_rank)
    return song_ranking_df

def get_artists() -> list:
    ranking_df = get_sql_data("ranking")
    artists = list(ranking_df["artist"].unique())
    artists_modified = []
    for artist in artists:
        artists_modified += artist.split(",")
    return artists_modified

def get_artist_page_link(wiki_type: str, artist_name: str) -> str:
    response = requests.get(f"https://kpop.fandom.com/wiki/Special:Search?query={artist_name}&scope={wiki_type}",
                            headers = {'User-Agent': UserAgent().chrome})
    soup = BeautifulSoup(response.text, 'lxml')
    results = soup.find_all("h3", class_="unified-search__result__header")
    link = "No link found"
    for i in range(0,3):
        #print(results[i].find_next_sibling("div").text)
        if artist_name.lower() in results[i].find_next_sibling("div").text.lower():
            link = results[i].find("a")["href"]
            break
    return link

def get_artist_info(link: str) -> pd.DataFrame:
    response = requests.get(link, headers = {'User-Agent': UserAgent().chrome})
    soup = BeautifulSoup(response.text, 'lxml')

    elements = soup.find_all("h2", class_="pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background")
    info_list = {}
    for element in elements:
        if element.text == "Background":
            infos = element.find_next_siblings("div")
            for info in infos:
                info_list[info.find("h3").text] = info.find("div").text
        elif element.text == "Career":
            infos = element.find_next_siblings("div")
            for info in infos:
                info_list[info.find("h3").text] = info.find("div").text
    return info_list
""" ------------------------------------------------------------------------------------------------- """

def clean_artist_name(rankings_df: pd.DataFrame):
    rankings_df["artist"] = rankings_df["artist"].str.split(",")
    artist_list = []
    for i in range(len(rankings_df)):
        for artist in rankings_df.loc[i, "artist"]:
            artist_list.append([i, artist])
    return pd.DataFrame(artist_list, columns=["index", "artist"])

def register_csv():
    get_kpop_rankings("weekly", date(2010,1,1), date.today()).to_csv("D:\Code\Kpop stats\kpop_rankings.csv", index = False)

rankings_df = pd.read_csv("D:\Code\Kpop stats\kpop_rankings.csv")
artist_ranking_df = clean_artist_name(rankings_df)
print(artist_ranking_df)
artist_ranking_df.to_csv("D:\Code\Kpop stats\kpop_ranking_artists.csv")