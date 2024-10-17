from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def search_wikipedia(query):

    browser.get("https://ru.wikipedia.org/")                                                               # Переходим на главную страницу русскоязычной Википедии
    search_box = browser.find_element(By.NAME, "search")                                             # Находим поле поиска по имени элемента
    search_box.clear()                                                                                     # Очищаем поле поиска на случай, если в нём уже есть текст
    search_box.send_keys(query)                                                                            # Вводим запрос, который пользователь хочет найти
    search_box.send_keys(Keys.RETURN)                                                                      # Нажимаем клавишу Enter для начала поиска
    time.sleep(3)                                                                                          # Ждём 3 секунды, чтобы страница успела загрузиться

def list_paragraphs():

    paragraphs = browser.find_elements(By.TAG_NAME, "p")                                             # Находим все элементы абзацев на странице
    for paragraph in paragraphs:
        print(paragraph.text)                                                                              # Печатаем текст каждого абзаца
        user_input = input("Нажмите Enter, чтобы продолжить, или введите 'exit', чтобы остановиться: ")    # Запрашиваем у пользователя ввод для продолжения или выхода
        if user_input.lower() == 'exit':
            break

def list_links():
    links = browser.find_elements(By.CSS_SELECTOR, "#bodyContent a[href^='/wiki/']")                 # Находим все ссылки, которые ведут на другие статьи Википедии
    for index, link in enumerate(links):
        print(f"{index}: {link.text}")                                                                     # Печатаем индекс и текст каждой ссылки
    return links

def main():
    global browser

    browser = webdriver.Firefox()                                                                          # Создаём экземпляр веб-драйвера Firefox
    try:
        while True:
            user_query = input("Введите запрос для поиска на Википедии (или введите 'exit' для выхода): ")   # Запрашиваем у пользователя ввод для поиска
            if user_query.lower() == 'exit':
                break

            search_wikipedia(user_query)                                                                     # Выполняем поиск по запросу
            while True:
                # Запрашиваем у пользователя выбор действия
                action = input("\nВыберите действие:\n1. Читать параграфы\n2. Перейти на связанные статьи\n3. Выйти в главное меню\nВведите ваш выбор (1/2/3): ")
                if action == '1':
                    # Чтение абзацев текущей статьи
                    list_paragraphs()
                elif action == '2':
                    links = list_links()                                                                          # Показать список связанных ссылок и перейти по выбранной
                    choice = input("\nВведите номер статьи, которую хотите посетить (или 'back' для возврата): ")
                    if choice.lower() == 'back':
                        continue
                    try:
                        index = int(choice)
                        if 0 <= index < len(links):
                            links[index].click()                                                                    # Переход по выбранной ссылке
                            time.sleep(3)                                                                           # Ждём, пока страница загрузится
                        else:
                            print("Неверный выбор. Попробуйте снова.")
                    except ValueError:
                        print("Неверный ввод. Пожалуйста, введите число.")
                elif action == '3':
                    break                                                                                           # Возврат в главное меню
                else:
                    print("Неверный выбор. Попробуйте снова.")
    finally:
        browser.quit()                                                                                              # Закрываем браузер при выходе из программы

if __name__ == "__main__":
    main()