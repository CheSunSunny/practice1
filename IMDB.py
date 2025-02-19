import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

from time import sleep


sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--verbose')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920, 1200')
chrome_options.add_argument('--disable-dev-shm-usage')

chromedriver_autoinstaller.install()

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.imdb.com/chart/top/")

links = driver.find_elements('xpath', "//a[contains(@class, 'ipc-title-link-wrapper')]")
print(links)
sleep(1)

uniq_links = set()
for i in links:
  uniq_links.add(i.get_attribute("href"))

print(len(uniq_links))  # столько фильмов на одной станице

sleep(1)
movies = driver.find_elements('xpath', "//h3[contains(@class, 'ipc-title__text')]")
uniq_movies = set()
for i in movies:
  if i.text[0].isdigit():
    uniq_movies.add(i.text.split(" ", maxsplit=1)[1])

print(len(uniq_movies))  # столько фильмов на одной станице
print(uniq_movies)

len(uniq_movies)

data = {}
for link in uniq_links:
    driver.get(link)
    try:
        title = driver.find_element('xpath', "//span[contains(@class, 'hero__primary-text')]").text
    except:
        pass
    else:
        if title in uniq_movies:
            synopsis = driver.find_element('xpath', "//span[contains(@data-testid, 'plot-xs_to_m')]").text
            rating = driver.find_element('xpath', "//span[contains(@class, 'sc-d541859f-1 imUuxf')]").text
            current_movie = {}
            current_movie["synopsis"] = synopsis
            current_movie["rating"] = rating
            current_movie["link"] = link
            data[title] = current_movie
            print(title, current_movie)
    sleep(1)  # нужен таймаут, чтобы драйвер успел перейти на новую страницу

print(data)
print(len(data))