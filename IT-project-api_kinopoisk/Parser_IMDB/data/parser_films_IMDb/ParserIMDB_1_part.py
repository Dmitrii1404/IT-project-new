# Открываю 1300 фильмов в подборке на imbd, сохраняю сайт html формате

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import fake_useragent

s = Service(
    executable_path=r"C:\Users\Dmitrii\Desktop\project it\data\chromedriver-win64\chromedriver.exe"
)  # Подключание драйвера браузера

useragent = fake_useragent.UserAgent().random  # создание useragent
options = webdriver.ChromeOptions()  # создание опций
options.add_argument(f"user-agent={useragent}")  # добавление в опции useragent
options.add_argument("--blink-settings=imagesEnabled=false")

driver = webdriver.Chrome(
    service=s, options=options
)  # Создание драйвера + передача опций

# Здесь я вручную выбираю какие страницы парсить
# url = 'https://www.imdb.com/search/title/?title_type=feature&user_rating=5,10&sort=num_votes,desc&num_votes=5000,'  # ссылка на страницу
# url = 'https://www.imdb.com/search/title/?title_type=feature&user_rating=5,10&sort=num_votes,desc&num_votes=5000,184100'
# url = 'https://www.imdb.com/search/title/?title_type=feature&user_rating=5,10&sort=num_votes,desc&num_votes=5000,90747'
# url = 'https://www.imdb.com/search/title/?title_type=feature&user_rating=5,10&sort=num_votes,desc&num_votes=5000,52275'
# url = 'https://www.imdb.com/search/title/?title_type=feature&user_rating=5,10&sort=num_votes,desc&num_votes=5000,33697'
url = "https://www.imdb.com/search/title/?title_type=feature&user_rating=5,10&sort=num_votes,desc&num_votes=5000,22920"

try:
    driver.maximize_window()  # Открываем окно на весь экран
    driver.get(url=url)
    time.sleep(5)
    count = 0
    while count < 25:
        if driver.find_elements(By.CLASS_NAME, "ipc-see-more"):
            button = driver.find_element(By.CLASS_NAME, "ipc-see-more")
            actoins = ActionChains(driver)
            actoins.move_to_element(button).perform()
            time.sleep(1)

            try:
                button.click()
                time.sleep(2)
            except:
                time.sleep(5)
                button.click()
                time.sleep(2)
            count += 1
            print(f"старница {count}")
        else:
            print("Страницы закончились")
            break

    time.sleep(3)


except Exception as ex:
    print(ex)
finally:
    # Будет несколько файлов по 1300 ссылок на фильм, поэтому в конце названия файла подпись с числом
    with open(
        "C:/Users/Dmitrii/Desktop/data/DB/movies6500.html", "w", encoding="UTF-8"
    ) as file:
        file.write(driver.page_source)
    time.sleep(10)
    driver.close()
    driver.quit()
