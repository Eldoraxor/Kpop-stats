import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

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
                    period: time,
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