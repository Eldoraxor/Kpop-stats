import pandas as pd
import requests
from bs4 import BeautifulSoup
import regex as re

def export_groups():
   response = requests.get('https://en.wikipedia.org/wiki/Category:K-pop_music_groups')
   soup = BeautifulSoup(response.text, 'lxml')

   page = soup.find("div", class_="mw-pages")
   print(page.content)
   next_page_link = page.find_next_sibling("a")
   print(next_page_link)
   for div in page.find_all("div", class_="mw-category-group"):
      for group in div.find_all("li"):
         groups = group.text
   return

export_groups()