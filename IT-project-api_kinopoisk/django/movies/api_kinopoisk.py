import requests
import json

headers = {"accept": "application/json", "X-API-KEY": "5J5BGMF-KN14VC9-HW608YR-W4A3P7X"}


# Самое главное, в фильтрах можно исключать категории "movies" - значит искать фильмы
# а "!movies" - не выводить фильмы
def search_by_id(id_):
    # Поиск фильма/сериала по id кинопоиска
    url = f"https://api.kinopoisk.dev/v1.4/movie/{id_}"
    response = requests.get(url, headers=headers)
    info = json.loads(response.text)  # Возвращаю только эту переменную,
    # при интегрировании апи в джанго, код ниже изменить как удобнее (мб перенести отсюдого в свой код)

    # Сам запрос сверху, снизу пример разложения информации по переменным
    name = info["name"]
    original_name = info["alternativeName"]
    type_ = info["type"]
    year = info["year"]
    description = info["description"]
    short_description = info["shortDescription"]
    slogan = info["slogan"]
    status = info["status"]  # Завершен сериал или нет? null/completed
    rating_kp = info["rating"]["kp"]
    rating_imdb = info["rating"]["imdb"]
    votes_kp = info["votes"]["kp"]
    votes_imdb = info["votes"]["imdb"]
    movie_length = info["movieLength"]  # null for serial
    series_length = info["seriesLength"]  # null for film
    age_rating = info["ageRating"]
    poster_full = info["poster"]["url"]
    poster_low = info["poster"]["previewUrl"]
    backdrop = info["backdrop"]["url"]

    genres = []
    for i in range(len(info["genres"])):
        genres.append(info["genres"][i]["name"])

    countries = []
    for i in range(len(info["countries"])):
        countries.append(info["countries"][i]["name"])

    actors = []
    directors = []
    producers = []
    for i in range(len(info["persons"])):
        if info["persons"][i]["enProfession"] == "actor":
            actors.append(info["persons"][i])  # id, photo, name, description
        elif info["persons"][i]["enProfession"] == "director":
            directors.append(info["persons"][i])  # id, photo, name, description
        elif info["persons"][i]["enProfession"] == "producer":
            producers.append(info["persons"][i])  # id, photo, name, description

    try:
        budget = str(info["budget"]["value"]) + str(info["budget"]["currency"])
    except:
        budget = None

    watchability = (
        []
    )  # где смотреть кинопоиск, иви и тд, тут название ресурса, его логотип и ссылка на фильм от туда
    for i in range(len(info["watchability"]["items"])):
        watchability.append(info["watchability"]["items"][i])  # name, logo -> url, url

    try:
        # год окончания сериала, если он завершен
        end_year = info["releaseYears"][0]["end"]
    except:
        end_year = None

    return info


def search_by_name(name_, page=1, limit=250):
    # поиск по названию
    # page = страница ответа, ну тип фильмы с первой страницы, со второй и тд
    # limit - количество выводимых фильмов, 250 - максимум, чтоб меньше запросов делать лучше по максимуму брать

    url = f"https://api.kinopoisk.dev/v1.4/movie/search?page={page}&limit={limit}&query={name_}"
    response = requests.get(url, headers=headers)
    info = json.loads(response.text)  # Возвращаю только эту переменную,
    # при интегрировании апи в джанго, код ниже изменить как удобнее (мб перенести отсюдого в свой код)

    # Сам запрос сверху, снизу пример разложения информации по переменным
    # Так как это поиск, фильмов выводится несколько, поэтому цикл
    for i in range(len(info["docs"])):

        name = info["docs"][i]["name"]
        original_name = info["docs"][i]["alternativeName"]
        year = info["docs"][i]["year"]

        genres = []
        for j in range(len(info["docs"][i]["genres"])):
            genres.append(info["docs"][i]["genres"][j]["name"])

        countries = []
        for j in range(len(info["docs"][i]["countries"])):
            countries.append(info["docs"][i]["countries"][j]["name"])

        id_ = info["docs"][i][
            "id"
        ]  # Этот id нужен, для того, чтоб потом открыть всю инфу о фильме с помощью первой функции в этом коде
        type_ = info["docs"][i]["type"]
        description = info["docs"][i]["description"]
        poster_full = info["docs"][i]["poster"]["url"]
        poster_low = info["docs"][i]["poster"]["previewUrl"]
        backdrop = info["docs"][i]["backdrop"]["url"]
        rating_kp = info["docs"][i]["rating"]["kp"]
        rating_imdb = info["docs"][i]["rating"]["imdb"]
        votes_kp = info["docs"][i]["votes"]["kp"]
        votes_imdb = info["docs"][i]["votes"]["imdb"]

    return info


def any_list(name_, page=1, limit=250):
    # Для вывода разных списков, топ250, топ лучших и тд
    # "popular-films", "top250", "top500", "series-top250", "popular-series" думаю этого нам хватит
    # name_ = top250 (пример)

    url = f"https://api.kinopoisk.dev/v1.4/movie/search?page={page}&limit={limit}&lists={name_}"
    response = requests.get(url, headers=headers)
    info = json.loads(response.text)  # Возвращаю только эту переменную,
    # при интегрировании апи в джанго, код ниже изменить как удобнее (мб перенести отсюдого в свой код)

    # Сам запрос сверху, снизу пример разложения информации по переменным
    # Так как это поиск, фильмов выводится несколько, поэтому цикл
    for i in range(len(info["docs"])):

        name = info["docs"][i]["name"]
        original_name = info["docs"][i]["alternativeName"]
        year = info["docs"][i]["year"]

        genres = []
        for j in range(len(info["docs"][i]["genres"])):
            genres.append(info["docs"][i]["genres"][j]["name"])

        countries = []
        for j in range(len(info["docs"][i]["countries"])):
            countries.append(info["docs"][i]["countries"][j]["name"])

        id_ = info["docs"][i]["id"]
        type_ = info["docs"][i]["type"]
        description = info["docs"][i]["description"]
        poster_full = info["docs"][i]["poster"]["url"]
        poster_low = info["docs"][i]["poster"]["previewUrl"]
        backdrop = info["docs"][i]["backdrop"]["url"]
        rating_kp = info["docs"][i]["rating"]["kp"]
        rating_imdb = info["docs"][i]["rating"]["imdb"]
        votes_kp = info["docs"][i]["votes"]["kp"]
        votes_imdb = info["docs"][i]["votes"]["imdb"]

    return info


# Здесь поиск по фильтрам, выводится список подходящих фильмов/сериалов
def search_by_filters(
    sort_field=None,
    sort_type=None,
    type_=None,
    year=None,
    rating_kp=None,
    votes_kp=None,
    age_rating=None,
    genres_name=None,
    is_series=None,
    countries_name=None,
    page=1,
    limit=250,
):
    # Если не заполнять фильтр, то его значение банально не будет учитываться
    # результат определяется только по заполненным фильтрам
    # Виды фильтров:
    # sortField=rating.kp/name/year/votes.kp - сортировка
    # sortType=1/-1 - сортировка по возрастанию/нет
    # type=movie/tv-series/cartoon/animated-series/anime - тип контента
    # year=1980 - год
    # rating.kp=8-10 - рейтинг кинопоиска от-до
    # votes.kp=10-90 - Количество голосов на кинопоиске от-до
    # ageRating=12-20 - возрастной рейтинг от-до
    # genres.name=драма - жанры
    # isSeries=true/false - сериал или нет
    # countries.name=страна - страна сериала
    if sort_type == None and sort_field != None:
        sort_type = 1  # Тк если выбрана сортировка, то обязательно должен быть выбран тип, по возрастанию или нет

    # пример вызова функции: search_by_filters(sort_field="name", rating_kp="8-10", year="2000")

    a = []
    a.append(("sortField=" + str(sort_field)) if sort_field != None else None)
    a.append(("sortType=" + str(sort_type)) if sort_type != None else None)
    a.append(("type=" + str(type_)) if type_ != None else None)
    a.append(("year=" + str(year)) if year != None else None)
    a.append(("votes.kp=" + str(rating_kp)) if rating_kp != None else None)
    a.append(("sortField=" + str(votes_kp)) if votes_kp != None else None)
    a.append(("ageRating=" + str(age_rating)) if age_rating != None else None)
    a.append(("genres.name=" + str(genres_name)) if genres_name != None else None)
    a.append(("isSeries=" + str(is_series)) if is_series != None else None)
    a.append(
        ("countries.name=" + str(countries_name)) if countries_name != None else None
    )

    filters = [i for i in a if i != None]
    url = f"https://api.kinopoisk.dev/v1.4/movie/search?page={page}&limit={limit}&{'&'.join(filters)}"
    response = requests.get(url, headers=headers)
    info = json.loads(response.text)  # Возвращаю только эту переменную,
    # при интегрировании апи в джанго, код ниже изменить как удобнее (мб перенести отсюдого в свой код)

    # Сам запрос сверху, снизу пример разложения информации по переменным
    # Так как это поиск, фильмов выводится несколько, поэтому цикл
    for i in range(len(info["docs"])):

        name = info["docs"][i]["name"]
        original_name = info["docs"][i]["alternativeName"]
        year = info["docs"][i]["year"]

        genres = []
        for j in range(len(info["docs"][i]["genres"])):
            genres.append(info["docs"][i]["genres"][j]["name"])

        countries = []
        for j in range(len(info["docs"][i]["countries"])):
            countries.append(info["docs"][i]["countries"][j]["name"])

        id_ = info["docs"][i]["id"]
        type_ = info["docs"][i]["type"]
        description = info["docs"][i]["description"]
        poster_full = info["docs"][i]["poster"]["url"]
        poster_low = info["docs"][i]["poster"]["previewUrl"]
        backdrop = info["docs"][i]["backdrop"]["url"]
        rating_kp = info["docs"][i]["rating"]["kp"]
        rating_imdb = info["docs"][i]["rating"]["imdb"]
        votes_kp = info["docs"][i]["votes"]["kp"]
        votes_imdb = info["docs"][i]["votes"]["imdb"]

    return info


# Здесь выводится информация о сезонах и сериях сериала, поиск сериала по его id
def about_the_episodes(id_, page=1, limit=250):
    url = f"https://api.kinopoisk.dev/v1.4/season?page={page}&limit={limit}&sortField=number&sortType=1&movieId={id_}"
    response = requests.get(url, headers=headers)
    info_ = json.loads(response.text)  # Возвращаю только эту переменную,
    # при интегрировании апи в джанго, код ниже изменить как удобнее (мб перенести отсюдого в свой код)

    # Сам запрос сверху, снизу пример разложения информации по переменным
    info = info_["docs"]

    for i in range(len(info)):
        # Цикл по сезонам
        season = info[i]["number"]

        for j in range(len(info[i]["episodes"])):
            # цикл по сериям в сезоне, для каждой есть свое описание
            number_eposode = info[i]["episodes"][j]["number"]

            try:
                description = info[i]["episodes"][j]["description"]
            except:
                description = None  # на всякий случай проверка

        description_season = info[i]["description"]  # а это описание всего сезона
        poster = info[i]["poster"]["url"]  # постер этого сезона

    return info
