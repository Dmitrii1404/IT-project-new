from bs4 import BeautifulSoup
import fake_useragent
import json
import requests
import time

pages = 200
list_urls = []
with open(
    "C:/Users/Dmitrii/Desktop/data/DB/book_urls.json", "a", encoding="UTF-8"
) as file:
    for i in range(100, pages + 1):
        f = f"https://mybook.ru/catalog/books/?o=readers&page={i + 1}"
        print(i)
        user = fake_useragent.UserAgent().random
        header = {"user-agent": user}
        responce = requests.get(
            f, headers=header
        ).text  # Получение страницы и передача user agent
        soup = BeautifulSoup(responce, "lxml")  # типа подключаем парсер
        urls = soup.find_all("div", class_="e4xwgl-0 iJwsmp")
        for url in urls:
            url_ = url.find("div", class_="e4xwgl-1 gEQwGK").find("a").get("href")
            list_urls.append(url_)
        time.sleep(1)

    json.dump(list_urls, file, indent=4, ensure_ascii=False)
