from datetime import time

import pytest
from selenium.webdriver.android import webdriver
from selenium.webdriver.common.by import By

from Data import email, password


@pytest.fixture(autouse=True)
def testing():
    with webdriver.Chrome() as driver:  # with - закрывает браузер в т.ч. при ошибке
        # Переходим на страницу авторизации
        driver.get('http://petfriends.skillfactory.ru/login')

        yield driver
        driver.quit()


def test_show_my_pets(testing):  # фикстуру добавляем в аргумент функции
    driver = testing  # транспортируем драйвер из фикстуры
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(password)
    time.sleep(2)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    time.sleep(2)

    """
    Мы объявили три переменные, в которых записали все найденные элементы на странице:
    в images — все картинки питомцев, в names — все их имена, в descriptions — все виды и возрасты.
    """
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''  # на странице нет питомцев без фото
        assert names[i].text != ''  # на странице нет питомцев без Имени
        assert descriptions[i].text != ''  # на странице нет питомцев с пустым полем для указания Породы и возраста
        assert ', ' in descriptions[i]  # проверяем, что между породой и лет есть запятая (значит есть оба значения)
        parts = descriptions[i].text.split(", ")  # Создаём список, где разделитель значений - запятая
        assert len(parts[0]) > 0  # Проверяем, что длина текста в первой части списка и
        assert len(parts[1]) > 0  # ...и во второй > 0, значит там что-то да указано! Если нет -> FAILED!

    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"  # Проверяем, что мы были на главной
    # есть утверждение для проверки заголовка страницы, что <title> Label содержит текст «PetFriends»:
    assert 'PetFriends' in driver.title  # да, работает