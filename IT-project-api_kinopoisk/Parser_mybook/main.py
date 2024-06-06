# Асинхронный парсер информации о фильмах IMDb, ссылки на которые расположены в файле
# Я лично считаю, что это имба. Имба на столько, что мне даже дали бан за слишком много запросов. Пришлось снизить обороты(((
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import fake_useragent
import json
import requests
import sqlite3


async def fetch(session, url, headers=None):
    async with session.get(url, headers=headers) as response:
        # Задержка отправления, чтоб не забанил сайт (и мб это помогает прогрузить номально страницу)
        await asyncio.sleep(2)
        return await response.text()


async def parse_film(session, url, conn, cur, semaphore, count_):
    max = 1100  # Ограничения для счетчика

    ISBN = ""  # Код книги
    Name = ""  # Название
    Page = ""  # Количество страниц
    Age = ""  # Возрастное ограничение
    URL = ""  # Ссылка
    Genres = []  # Жанры
    Topic = []  # Тема
    Rating = ""  # Оценка
    Number_of_ratings = ""  # Количество оценок
    Description = ""  # Описание
    Author = ""  # Автор
    Similars = []  # Похожие книги

    user = fake_useragent.UserAgent().random
    header = {"user-agent": user}
    URL = "https://mybook.ru/" + url
    cur.execute("SELECT * FROM books WHERE URL = ?", (url,))
    result = cur.fetchone()
    if (
        count_ <= max and result == None
    ):  # чтоб ноут долго не простаивал, парсинг разделяю на части, так что условие name <= max просто для моего удобства
        try:
            async with semaphore:
                html = await fetch(session, URL, headers=header)
            soup = BeautifulSoup(html, "lxml")
            print(f"Iteration: {count_}")

            try:
                some_info = soup.find("div", class_="ant-row sc-1c0xbiw-1 cyJjtq")
                Name = some_info.find("div", class_="m4n24q-0 hJyrxa").text
                Author = some_info.find("div", class_="dey4wx-1 jVKkXg").text
            except:
                pass

            try:
                some_info = soup.find("div", class_="ant-row sc-1c0xbiw-1 cyJjtq")
                some_info = some_info.find("div", class_="ant-col sc-1c0xbiw-9 eSjGMZ")
                Page = some_info.find_all("p", class_="lnjchu-1 dPgoNf")[0].text
                if "печат" not in Page:
                    Page = "Неизвестно"
                Age = some_info.find_all("p", class_="lnjchu-1 dPgoNf")[3].text
            except:
                pass

            try:
                some_info = soup.find("div", class_="ant-col sc-1c0xbiw-5 lotch")
                Rating = some_info.find("div", class_="sc-1s4c57r-0 goYpPi").text
                Number_of_ratings = some_info.find(
                    "div", class_="sc-1c0xbiw-6 cyZcfr"
                ).text
            except:
                pass

            try:
                some_info = soup.find("div", class_="iszfik-14 iSnZQd")
                some_info_2 = some_info.find_all("div", class_="iszfik-15 BerVK")[1]
                ISBN = some_info_2.find_all("dd", class_="iszfik-18 iEusfO")[0].text
                try:
                    a = int(ISBN)
                except:
                    ISBN = ""
            except:
                pass

            try:
                some_info = soup.find_all("div", class_="sc-1sg8rha-0 gHinNz")
                some_info_1 = some_info[0].find_all("div", class_="sc-1sbv3y7-0 bQSldI")
                for genre in some_info_1:
                    Genres.append(genre.text)

                some_info_2 = some_info[1].find_all("div", class_="sc-1sbv3y7-0 bQSldI")
                for tp in some_info_2:
                    Topic.append(tp.text)
            except:
                pass

            try:
                some_info = soup.find("div", class_="iszfik-2 gAFRve")
                Description = some_info.text
            except:
                pass

            try:
                some_info = soup.find(
                    "div", class_="m4n24q-0 dsNpLo cy-similar-content-slider"
                )
                some_info = some_info.find(
                    "div", class_="sc-1hf4y1s-2 bTSqUP swiper-wrapper"
                )
                some_info = some_info.find_all(
                    "div", class_="swiper-slide sc-12qqvjh-0 gzajCe"
                )
                for info in some_info:
                    similar = (
                        info.find("div", class_="sc-7dmtki-0").find("a").get("href")
                    )
                    Similars.append(similar)
            except:
                pass

            try:
                photo_ = (
                    soup.find("div", class_="hh1ehr-0 kkiIwl")
                    .find("picture")
                    .find("img")
                )
                imglink = photo_.get("srcset").split(", ")[0]
                image = requests.get(imglink).content
                with open(
                    r"C:/Users/Dmitrii/Desktop/data/imagine_books/" + Name + ".jpg",
                    "wb",
                ) as imgfile:
                    imgfile.write(image)
            except:
                pass

            print(ISBN, Name, Rating)  # чтоб понимать, парсится или нет
            cur.execute(
                f"""INSERT INTO books(
                ISBN,
                Name,
                Page,
                Age,
                URL,
                Genres,
                Topic,
                Rating,
                Number_of_ratings,
                Description,
                Author,
                Similars) 
                              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    ISBN,
                    Name,
                    Page,
                    Age,
                    url,
                    ",".join(Genres),
                    ",".join(Topic),
                    Rating,
                    Number_of_ratings,
                    Description,
                    Author,
                    ",".join(Similars),
                ),
            )
            conn.commit()

        except Exception as e:
            print(f"Error parsing {Name}: {e}")

    elif count_ <= max:
        count_ += 1
        print(f"Книга с ссылкой {url} уже есть в дб")


async def main():
    semaphore = asyncio.Semaphore(
        15
    )  # Ограничение на количество одновременно выполняемых задач
    async with aiohttp.ClientSession() as session:
        with open(
            "C:/Users/Dmitrii/Desktop/data/DB/book_urls.json", "r", encoding="UTF-8"
        ) as file:
            all_films = json.load(file)

        conn = sqlite3.connect("C:/Users/Dmitrii/Desktop/data/DB/books_info.db")
        cur = conn.cursor()
        cur.execute(
            """
               CREATE TABLE IF NOT EXISTS books (
               ISBN TEXT NOT NULL,
               Name TEXT NOT NULL,
               Page TEXT NOT NULL,
               Age TEXT NOT NULL,
               URL TEXT NOT NULL,
               Genres TEXT NOT NULL,
               Topic TEXT NOT NULL,
               Rating TEXT NOT NULL,
               Number_of_ratings TEXT NOT NULL,
               Description TEXT NOT NULL,
               Author TEXT NOT NULL,
               Similars TEXT NOT NULL
               )
               """
        )
        conn.commit()
        tasks = []
        count = 0
        for url in all_films:
            count += 1
            tasks.append(parse_film(session, url, conn, cur, semaphore, count))

        await asyncio.gather(*tasks)

        conn.close()


async def run_main():
    await main()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_main())
