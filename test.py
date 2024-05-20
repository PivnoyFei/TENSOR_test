import os
from typing import Any, Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from pageobjects import (
    AboutPage,
    ContactsLocationPage,
    DownloadPlugin,
    SbisContactsPage,
    TensorPage,
)
from settings import settings


@pytest.fixture
def browser() -> Generator[WebDriver, Any, None]:
    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": settings.BASE_DIR,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_check_images_height_and_width(browser: WebDriver) -> None:
    sbis_contacts_page = SbisContactsPage(browser)

    # Переходим на сайт sbis.ru и открываем раздел "Контакты"
    sbis_contacts_page.find_element_and_clickable(settings.CONTACTS_LINK)

    # Находим и кликаем по баннеру Тензор
    sbis_contacts_page.click_tensor_banner()

    # Переходим на сайт tensor.ru
    tensor_page = TensorPage(browser, sbis_contacts_page.driver.current_url)

    # Проверяем наличие блока "Сила в людях"
    assert settings.POWER_IN_PEOPLE in tensor_page.is_power_in_people_block()

    # Переходим в блок "Сила в людях" и открываем "Подробнее"
    tensor_page.find_element_and_clickable(settings.ABOUT_LINK)

    # Проверяем, что открылась страница https://tensor.ru/about
    assert settings.TENSOR_ABOUT_URL in tensor_page.driver.current_url

    # Проверяем, что у всех фотографий в разделе "Работаем" одинаковая высота и ширина
    about_page = AboutPage(browser, tensor_page.driver.current_url)
    assert about_page.are_images_dimensions_equal()


def test_region_change(browser: WebDriver) -> None:
    contacts_page = ContactsLocationPage(browser)
    contacts_page.find_element_and_clickable(settings.CONTACTS_LINK)

    # Проверяем, что определился ваш регион (в нашем примере Ярославская обл.) и есть список партнеров
    assert contacts_page.is_region_correct() == settings.MY_REGION
    region_partners = contacts_page.find_elements(settings.REGION_PARTNERS)

    # Изменяем регион на Камчатский край
    contacts_page.change_region(settings.NEW_REGION)

    # Проверяем, что регион изменился, список партнеров обновился и URL, title содержат информацию о выбранном регионе
    assert contacts_page.is_region_correct() == settings.NEW_REGION
    assert region_partners != contacts_page.find_elements(settings.REGION_PARTNERS)
    assert settings.URL_NEW_REGION in browser.current_url
    assert settings.NEW_REGION in browser.title


def test_download_plugin(browser: WebDriver) -> None:
    footer = DownloadPlugin(browser)

    # Находим ссылку в Footer'e по тексту и кликаем на нее
    footer.open_footer_link()

    # Скачиваем файл по ссылке
    stated_size, download_size, filename = footer.download_file()

    # # Проверяем размер скачанного файла
    assert download_size == pytest.approx(stated_size, rel=0.1)

    if os.path.exists(filename):
        os.remove(filename)
