# Асинхронный парсер информации о фильмах IMDb, ссылки на которые расположены в файле
# Я лично считаю, что это имба. Имба на столько, что мне даже дали бан за слишком много запросов. Пришлось снизить обороты(((
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import fake_useragent
import json
import requests
import sqlite3

count_ = 0


async def fetch(session, url, headers=None):
    async with session.get(url, headers=headers) as response:
        # Задержка отправления, чтоб не забанил сайт (и мб это помогает прогрузить номально страницу)
        await asyncio.sleep(1)
        return await response.text()


async def parse_film(session, name, url, conn, cur, semaphore):
    global count_
    max = 10
    photo_url = ""

    name = name.split(".")[0]  # Получаем номер фильма из списка
    Run_time = ""  # Продолжительность фильма
    genres = []  # Список жанров
    rating = ""  # Оценка
    number_of_ratings = ""  # Количество оценок
    description = ""  # Описание
    Release_date = ""  # Дата релиза
    Country = []  # Страна
    Budget = ""  # Бюджет
    Director = ""  # Режисер
    Writer = ""  # Сценарист
    Actors = []  # Актеры
    key_words = []  # Ключевые слова
    similars = []  # Похожие фильмы

    user = fake_useragent.UserAgent().random
    header = {"user-agent": user}
    f = list(url.split("/"))
    h = f[4]
    f = "/".join(f[:5])  # Отрезаю лишнюю часть от ссылки
    URL_ = f  # Сохраняю ссылку

    cur.execute("SELECT * FROM films WHERE tag = ?", (h,))
    result = cur.fetchone()

    if (
        int(name) <= max and result == None
    ):  # чтоб ноут долго не простаивал, парсинг разделяю на части, так что условие name <= max просто для моего удобства
        try:
            async with semaphore:
                html = await fetch(session, f, headers=header)
            soup = BeautifulSoup(html, "lxml")

            count_ += 1
            print(f"Iteration: {count_}")

            try:
                photo_url_ = soup.find_all(
                    "a", class_="ipc-lockup-overlay ipc-focusable"
                )[0]
                photo_url = "https://www.imdb.com" + photo_url_.get("href")
            except:
                pass

            try:
                Name = soup.find("span", class_="hero__primary-text").text
            except:
                pass

            try:
                description = soup.find("span", class_="sc-a31b0662-0 iBnSmy").text
            except:
                pass

            try:
                genres_html = soup.find_all("a", class_="ipc-chip ipc-chip--on-baseAlt")
                for genre in genres_html:
                    genres.append(genre.text)
            except:
                pass

            try:
                rating = soup.find("span", class_="sc-bde20123-1 cMEQkK").text
                rating = rating.replace(".", ",")
                print(rating)
            except:
                print("не")
                pass

            try:
                number_of_ratings = soup.find("div", class_="sc-bde20123-3 gPVQxL").text
            except:
                pass

            try:
                some_info = soup.find_all(
                    "ul",
                    class_="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base",
                )[1]
                some_info = some_info.find_all("li", class_="ipc-metadata-list__item")
            except:
                pass

            try:
                Release_date = (
                    some_info[0]
                    .find(
                        "a",
                        class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link",
                    )
                    .text
                )
            except:
                pass

            try:
                C = some_info[1].find_all(
                    "a",
                    class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link",
                )
                for co in C:
                    Country.append(co.text)
            except:
                pass

            try:
                Budget = soup.find_all(
                    "li", class_="ipc-metadata-list__item sc-1bec5ca1-2 bGsDqT"
                )
                Budget = (
                    Budget[0]
                    .find("span", class_="ipc-metadata-list-item__list-content-item")
                    .text
                )
            except:
                pass

            try:
                info = soup.find(
                    "ul",
                    class_="ipc-metadata-list ipc-metadata-list--dividers-all sc-bfec09a1-8 bHYmJY ipc-metadata-list--base",
                )
                info = info.find_all(
                    "a",
                    class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link",
                )
                Writer = info[1].text
                Director = info[0].text
            except:
                pass

            try:
                info = soup.find_all("div", class_="sc-bfec09a1-7 gWwKlt")
                for actor in info:
                    actor_name = actor.find("a", class_="sc-bfec09a1-1 gCQkeh").text
                    actor_role = actor.find("span", class_="sc-bfec09a1-4 kvTUwN").text
                    Actors.append([actor_name, actor_role])
            except:
                pass

            try:
                Run_time = soup.find(
                    "ul",
                    class_="ipc-metadata-list ipc-metadata-list--dividers-none ipc-metadata-list--compact ipc-metadata-list--base",
                )
                Run_time = (
                    Run_time.find("li", class_="ipc-metadata-list__item")
                    .find("div", class_="ipc-metadata-list-item__content-container")
                    .text
                )
            except:
                pass

            try:
                similars_html = soup.find_all(
                    "div",
                    class_="ipc-poster-card ipc-poster-card--base ipc-poster-card--dynamic-width ipc-sub-grid-item ipc-sub-grid-item--span-2",
                )
                for s in similars_html:
                    similar = s.find(
                        "a",
                        class_="ipc-poster-card__title ipc-poster-card__title--clamp-2 ipc-poster-card__title--clickable",
                    ).get("href")
                    similar = similar.split("/")[2]
                    similars.append(similar)
            except:
                pass

            try:
                Name = soup.find("span", class_="hero__primary-text").text
            except:
                pass

            res = requests.get(
                photo_url, headers=header
            ).text  # Получение страницы и передача user agent
            soup = BeautifulSoup(res, "lxml")

            photo_ = soup.find_all("div", class_="sc-7c0a9e7c-2 ghbUKT")[0]
            img = photo_.find("img")

            try:
                imglink = img.get("srcset").split()[2]
                image = requests.get(imglink).content
                with open(
                    r"C:/Users/Dmitrii/Desktop/data/DB/imagine/" + h + ".jpg", "wb"
                ) as imgfile:
                    imgfile.write(image)
            except:
                imglink = img.get("src")
                print(imglink)
                image = requests.get(imglink).content
                with open(
                    r"C:/Users/Dmitrii/Desktop/data/imagine/" + h + ".jpg", "wb"
                ) as imgfile:
                    imgfile.write(image)

            try:
                f = f + "/keywords"
                res = requests.get(
                    f, headers=header
                ).text  # Получение страницы и передача user agent
                soup = BeautifulSoup(res, "lxml")
                key_words_html = soup.find_all(
                    "div", class_="ipc-metadata-list-summary-item__tc"
                )
                for word in key_words_html:
                    key_words.append(word.text)  # Сохранение ключевых слов
            except Exception as e:
                print(f"Error parsing keywords for {name}: {e}")

            cur.execute(
                f"""INSERT INTO films(
                tag,
                Name,
                URL,
                Runtime,
                Genres,
                Rating,
                Number_of_ratings,
                Description,
                Release_date,
                Country,
                Budget,
                Director,
                Writer,
                Actors,
                key_words,
                Similars)
                              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    h,
                    Name,
                    URL_,
                    Run_time,
                    ", ".join(genres),
                    rating,
                    number_of_ratings,
                    description,
                    Release_date,
                    ", ".join(Country),
                    Budget,
                    Director,
                    Writer,
                    "; ".join(",".join(i) for i in Actors),
                    ", ".join(key_words),
                    ", ".join(similars),
                ),
            )
            conn.commit()

        except Exception as e:
            print(f"Error parsing {name}: {e}")

    elif int(name) <= max:
        print(f"Фильм с тегом {h} уже есть в дб")


async def main():
    semaphore = asyncio.Semaphore(
        10
    )  # Ограничение на количество одновременно выполняемых задач
    async with aiohttp.ClientSession() as session:
        with open(
            "C:/Users/Dmitrii/Desktop/data/DB/movie_URL_IMDb.json",
            "r",
            encoding="UTF-8",
        ) as file:
            all_films = json.load(file)

        conn = sqlite3.connect("C:/Users/Dmitrii/Desktop/data/DB/films_info.db")
        cur = conn.cursor()
        cur.execute(
            """
               CREATE TABLE IF NOT EXISTS films (
               tag TEXT PRIMARY KEY,
               Name TEXT NOT NULL,
               URL TEXT NOT NULL,
               Runtime TEXT NOT NULL,
               Genres TEXT NOT NULL,
               Rating TEXT NOT NULL,
               Number_of_ratings TEXT NOT NULL,
               Description TEXT NOT NULL,
               Release_date TEXT NOT NULL,
               Country TEXT NOT NULL,
               Budget TEXT NOT NULL,
               Director TEXT NOT NULL,
               Writer TEXT NOT NULL,
               Actors TEXT NOT NULL,
               key_words TEXT NOT NULL,
               Similars TEXT NOT NULL
               )
               """
        )
        conn.commit()
        tasks = []
        for name, url in all_films.items():
            tasks.append(parse_film(session, name, url, conn, cur, semaphore))

        await asyncio.gather(*tasks)

        conn.close()


async def run_main():
    await main()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_main())
