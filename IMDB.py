import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

from time import sleep
import json


sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--verbose')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920, 1200')
chrome_options.add_argument('--disable-dev-shm-usage')

chromedriver_autoinstaller.install()

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.imdb.com/chart/top/")

links = driver.find_elements('xpath', "//a[contains(@class, 'ipc-title-link-wrapper')]")
print("ссылки со страницы: ", links)
sleep(1)

uniq_links = set()
for i in links:
    uniq_links.add(i.get_attribute("href"))

print(len(uniq_links), "ссылок на одной странице")  # столько фильмов на одной странице

sleep(1)
movies = driver.find_elements('xpath', "//h3[contains(@class, 'ipc-title__text')]")
uniq_movies = set()
for i in movies:
    if i.text[0].isdigit():
        uniq_movies.add(i.text.split(" ", maxsplit=1)[1])

print(len(uniq_movies), "фильмов на одной странице")  # столько фильмов на одной странице
print("уникальные фильмы: ", uniq_movies)

data = {}
for link in uniq_links:
    driver.get(link)
    try:
        title = driver.find_element('xpath', "//span[contains(@class, 'hero__primary-text')]").text
    except:
        pass
    else:
        if title in uniq_movies:
            synopsis = driver.find_element('xpath', "//p[contains(@data-testid, 'plot')]").text
            rating = driver.find_element('xpath', "//span[contains(@class, 'sc-d541859f-1 imUuxf')]").text
            year = driver.find_element('xpath', "//a[contains(@href, 'releaseinfo')]").text
            genre = driver.find_element('xpath', "//div[contains(@class, 'ipc-chip-list__scroller')]").text
            director = driver.find_element('xpath', "//a[contains(@href, 'name')]").text
            current_movie = {}
            current_movie["year"] = year
            current_movie["genre"] = genre
            current_movie["synopsis"] = synopsis
            current_movie["director"] = director
            current_movie["rating"] = rating
            current_movie["link"] = link


            data[title] = current_movie
    sleep(1)  # нужен таймаут, чтобы драйвер успел перейти на новую страницу

print("полученные данные: ", data)
print("количество данных: ", len(data))

with open("imdb_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
