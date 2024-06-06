import account_login
import account_info

global username  # Сохраняем username пользователя


def login():
    global username
    username = account_login.login_()
    return username


def registration():
    global username
    username = account_login.registration()
    return username


if __name__ == "__main__":
    username = ""
    while True:
        print("Что вы хотите сделать?")
        i_want = input().lower()
        if i_want == "войти в аккаунт":
            print(login())
        elif i_want == "зарегестрироваться":
            print(registration())
        elif i_want == "предпочтения":
            if username != "":
                print(account_login.account_info(username))
            else:
                print("Войдите в аккаунт")
        elif i_want == "оценка":
            if username != "":
                tag = input()
                account_info.reviews_film(tag, username)
            else:
                print("Войдите в аккаунт")
        elif i_want == "поменять логин":
            if username != "":
                account_login.change_username(username)
            else:
                print("Войдите в аккаунт")
        elif i_want == "уйти":
            break
