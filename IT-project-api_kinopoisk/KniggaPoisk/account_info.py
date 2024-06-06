# тег фильма / username - просмотрен / отзыв / оценка
import sqlite3


def reviews_film(tag, username):
    conn = sqlite3.connect(r"database\reviews_film.db")
    cur = conn.cursor()
    cur.execute(
        """
           CREATE TABLE IF NOT EXISTS (
           tag TEXT NOT NULL,
           username TEXT NOT NULL,
           review TEXT NOT NULL,
           rating TEXT NOT NULL
           )
           """
    )
    conn.commit()
    # Будем считать, что если человек пишет отзыв, то он смотрел фильм
    print("Напишите свое мнение о фильме: ", end="")
    review = input()
    print("Ваша оценка от 1 до 10: ", end="")
    while True:
        try:
            rating = int(input())
            if 1 <= rating <= 10:
                break
            else:
                print("Оценка от 1 до 10!!!")
        except:
            print("Неверный формат ввода, введите целое число!")

    cur.execute("SELECT * FROM reviews WHERE tag=? AND username = ?", (tag, username))
    result = cur.fetchone()
    if result == None:
        cur.execute(
            f"""INSERT INTO reviews(tag, username, review, rating)
                      VALUES(?, ?, ?, ?)""",
            (tag, username, review, rating),
        )
        conn.commit()
    else:
        cur.execute(
            f"""UPDATE reviews SET review=?, rating=? WHERE tag=? AND username=?""",
            (review, rating, tag, username),
        )
        conn.commit()
    conn.close()
