import os

from selenium.webdriver.common.by import By


class ContactsPageSettings:
    CONTACTS_LINK = (By.CSS_SELECTOR, '[href="/contacts"]')
    TENSOR_BANNER = (By.CSS_SELECTOR, '[title="tensor.ru"]')


class TensorPageSettings:
    ABOUT_LINK = (By.CSS_SELECTOR, '[href="/about"]')
    IS_POWER_IN_PEOPLE_BLOCK = (By.CSS_SELECTOR, "div.tensor_ru-Index")


class AboutPageSettings:
    BLOCK_IMAGE = (
        By.CSS_SELECTOR,
        "div.tensor_ru-container.tensor_ru-section.tensor_ru-About__block3",
    )
    TAG_IMAGE = (By.TAG_NAME, "img")


class LocationPageSettings:
    REGION_NOW = (By.CSS_SELECTOR, ".sbis_ru-Region-Chooser__text")
    REGION_PARTNERS = (By.CSS_SELECTOR, ".sbisru-Contacts-List__item")


class DownloadPluginSettings:
    FOOTER_LINK_TEXT = (By.LINK_TEXT, "Скачать локальные версии")
    LINK_TEXT_SBIS_PLAGIN = (By.LINK_TEXT, "СБИС Плагин")
    LINK_DOWNLOAD_TEXT_SBIS_PLAGIN = "Веб-установщик"
    LINK_SBIS_PLAGIN = (By.CSS_SELECTOR, "div.controls-TabButton")
    LINK_DOWNLOAD = (
        By.CSS_SELECTOR,
        "div.sbis_ru-DownloadNew-block.sbis_ru-DownloadNew-flex",
    )
    LINK_TEXT_DOWNLOAD = (By.PARTIAL_LINK_TEXT, "Скачать")


class Settings(
    ContactsPageSettings,
    TensorPageSettings,
    AboutPageSettings,
    LocationPageSettings,
    DownloadPluginSettings,
):
    SBIS_URL = "https://sbis.ru/"
    TENSOR_ABOUT_URL = "https://tensor.ru/about"
    POWER_IN_PEOPLE = "Сила в людях"
    MY_REGION = "Нижегородская обл."
    NEW_REGION = "Камчатский край"
    URL_NEW_REGION = "kamchatskij-kraj"
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))


settings = Settings()
