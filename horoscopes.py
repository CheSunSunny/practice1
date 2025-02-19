import requests
from bs4 import BeautifulSoup  # библиотека для парсинга
import json

# создаём словарь с названиями знаков на англ и рус
signs = {"aries": "Овен",
         "taurus": "Телец",
         "gemini": "Близнецы",
         "cancer": "Рак",
         "leo": "Лев",
         "virgo": "Дева",
         "libra": "Весы",
         "scorpio": "Скорпион",
         "sagittarius": "Стрелец",
         "capricorn": "Козерог",
         "aquarius": "Водолей",
         "pisces": "Рыбы"}
horoscope = {}  # создаём словарь, в который будем сохранять данные
# перебираем ключи словаря со знаками
for i, sign in enumerate(signs):

    sign_name = signs[sign]  # находим имя знака на рус (обращаемся к словарю знаков по ключу)
    horoscope[sign_name] = {}  # создаём элемент словаря данных с ключом в виде названия знака на рус

    # переходим на страницу с гороскопом для знака на неделю
    url = f'https://1001goroskop.ru/?znak={sign}&kn=week'
    headers = {
        'User-Agent': 'My User Agent 1.0',  # многие сайты не дают себя парсить ботам
    }
    response = requests.get(url, headers=headers)

    page = response.text
    soup_d = BeautifulSoup(page, "html.parser")
    description = soup_d.find("div", {"itemprop": "description"})  # находим тэг с описанием
    dates = description.find_all("div", {"class": "date"})  # находим все тэги с датой

    # перебираем найденные тэги
    for d in dates:
        date = d.text  # дата (ключ словаря) - текст из тэга
        prediction = d.find_next('p').text  # предсказание (содержимое словаря) - следующий за тэгом с датой параграф
        horoscope[sign_name][date] = prediction  # записываем в словарь элемент с ключом-датой и содержимым-описанием

# создаём и открываем файл json, записываем туда словарь с данными в формате json
with open("horoscope_data.json", "w", encoding="utf-8") as f:
    json.dump(horoscope, f, ensure_ascii=False, indent=4)

# открываем файл, чтобы проверить, что всё сработало
with open("horoscope_data.json", "r", encoding="utf-8") as f:
    from_file = json.load(f)

# печатаем элемент json
print(from_file["Дева"])
