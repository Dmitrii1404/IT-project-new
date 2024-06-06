import hashlib
import sqlite3


# Проверка на наличие символов в строке
def check_sumbol():
    str_ = input()
    if str_ == "":
        print("Ошибка, введена пустая строка, попробуйте заново")
        return check_sumbol()
    else:
        return str_


# Проверка, есть ли данный username в бд
def check_username(username):
    conn = sqlite3.connect(r"database\account_info.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE username=?", (username,))
    result = cur.fetchone()
    if result == None:
        return True
    else:
        return False


# Регистрация аккаунта
def registration(username="", login=""):
    conn = sqlite3.connect(r"database\account_info.db")
    cur = conn.cursor()
    cur.execute(
        """
       CREATE TABLE IF NOT EXISTS Users (
       username TEXT PRIMARY KEY,
       login TEXT NOT NULL,
       password TEXT NOT NULL
       )
       """
    )
    conn.commit()
    print("Регистрация")
    if username == "":
        while True:
            print("Имя:", end=" ")
            username = check_sumbol()
            if check_username(username):
                print("Логин:", end=" ")
                login = check_sumbol()
                login = hashlib.sha1(login.encode()).hexdigest()
                break
            else:
                print("Данный username занят(((")

    print("Пароль:", end=" ")
    password1 = check_sumbol()
    password1 = hashlib.sha1(password1.encode()).hexdigest()
    print("Введите пароль еще раз:", end=" ")
    password2 = hashlib.sha1(input().encode()).hexdigest()
    if password1 != password2:
        print("Ошибра, пароли не совпадают, попробуйте еще раз")
        conn.close()
        return registration(username, login)
    else:
        cur.execute(
            f"""INSERT INTO users(username, login, password)
              VALUES(?, ?, ?)""",
            (username, login, password2),
        )
        conn.commit()
        conn.close()
        print("Вы успешно зарегестрированы")
        return username


# Вход в аккаунт
def login_():
    conn = sqlite3.connect(r"database\account_info.db")
    cur = conn.cursor()
    # Вход в аккаунт
    print("Вход в аккаунт")
    print("Логин:", end=" ")
    login = hashlib.sha1(input().encode()).hexdigest()
    print("Пароль:", end=" ")
    password = hashlib.sha1((input()).encode()).hexdigest()
    cur.execute("SELECT * FROM Users WHERE login = ?", (login,))
    result = cur.fetchone()
    if result != None and password == result[2]:
        print("Вы успешно зашли в аккаунт")
        username = result[0]
        conn.close()
        return username
    else:
        print("Логин или пароль неверен")
        conn.close()
        return login_()


# Добавление информации о предпочтениях
def account_info(username):
    conn = sqlite3.connect(r"database\account_info.db")
    cur = conn.cursor()
    cur.execute(
        """
           CREATE TABLE IF NOT EXISTS Users_info (
           username TEXT PRIMARY KEY,
           likes_genre TEXT NOT NULL,
           age TEXT NOT NULL
           )
           """
    )
    conn.commit()
    likes_genre = ""
    genres = [
        "биография",
        "боевик",
        "вестерн",
        "военный",
        "детектив",
        "документальный",
        "драма",
        "исторический",
        "комедия",
        "короткометражка",
        "криминал",
        "мелодрама",
        "мюзикл",
        "приключения",
        "семейный",
        "спорт",
        "триллер",
        "ужасы",
        "фантастика",
        "фэнтези",
    ]
    print("Какие жанры вы предпочитаете?")
    while True:
        genre = input().lower()
        if genre in genres:
            likes_genre += "," + genre
        print("Еще какие то?")
        x = input().lower()
        if x == "нет":
            break
    print("Введите ваш возраст:", end=" ")
    age = int(input())
    cur.execute(
        f"""INSERT INTO users_info(username, likes_genre, age)
                  VALUES(?, ?, ?)""",
        (username, likes_genre, age),
    )
    conn.commit()
    conn.close()
    return username


# Подключение бд для изменения username
def change_username(username):
    print("Введите новый username: ", end="")
    while True:
        new_username = input()
        if check_username(new_username):
            break
        else:
            print("Данный username занят(((")

    conn1 = sqlite3.connect(r"database\account_info.db")
    cur1 = conn1.cursor()
    name_table = "users_info"
    change_username_(username, new_username, conn1, cur1, name_table)
    name_table = "users"
    change_username_(username, new_username, conn1, cur1, name_table)

    conn2 = sqlite3.connect(r"database\reviews_film.db")
    cur2 = conn2.cursor()
    name_table = "reviews"
    change_username_(username, new_username, conn2, cur2, name_table)

    conn1.close()
    conn2.close()


# Изменение username
def change_username_(username, new_username, conn, cur, name_table):
    cur.execute(f"SELECT * FROM {name_table} WHERE username = ?", (username,))
    result = cur.fetchone()
    if result != None:
        cur.execute(
            f"""UPDATE {name_table} SET username=? WHERE username=?""",
            (new_username, username),
        )
        conn.commit()
