# Из html кода, полученного после ParserIMDB_1_part собираю ссылки на фильмы и сохраняю их в json
from bs4 import BeautifulSoup
import json

with open(
    "C:/Users/Dmitrii/Desktop/data/DB/movies6500.html", "r", encoding="UTF-8"
) as file:  # Вречную подписываю число в конце названия файла, тк их несколько
    f = file.read()

soup = BeautifulSoup(f, "lxml")  # типа подключаем парсер
movies_inf = soup.find_all("div", class_="sc-d80c3c78-4 kXzHjH dli-parent")

dict_movies = {}
for inf in movies_inf:
    url_ = inf.find(
        "div",
        class_="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b0691f29-9 klOwFB dli-title",
    ).find("a")
    url = "https://www.imdb.com" + url_.get("href")
    name = url_.find("h3", class_="ipc-title__text").text
    name = list(name.split(". "))
    name = (
        str(6500 + int(name[0])) + ". " + ". ".join(name[1:])
    )  # Число в начале - это число из названия файла, сделано, чтоб нумерация фильмов не сбилась
    dict_movies[name] = url

with open(
    "C:/Users/Dmitrii/Desktop/data/DB/movie_URL_IMDb.json", "a", encoding="UTF-8"
) as file:
    json.dump(dict_movies, file, indent=4, ensure_ascii=False)
