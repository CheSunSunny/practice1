import requests
import json

# базовые данные для формирования запроса
VK_CONFIG = {
    "domain": "https://api.vk.com/method",
    "access_token": "",
    "version": "5.199",

}

wall_domain = "panhck"
count = 100
offset = [0, 100, 200]
posts=[]
for shift_size in offset:
    query = f"{VK_CONFIG['domain']}/wall.get?access_token={VK_CONFIG['access_token']}&domain={wall_domain}&offset={shift_size}&v={VK_CONFIG['version']}&count={count}"
    response = requests.get(query)
    posts+=[res["text"] for res in response.json()["response"]["items"]]
with open("vk_posts.json", "w", encoding="utf-8") as f:
    to_save = {n: post for n, post in enumerate(posts)}
    json.dump(to_save, f, ensure_ascii=False, indent=4)
