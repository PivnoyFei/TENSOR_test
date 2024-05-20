import os
import re
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings import settings


class BasePage:
    def __init__(
        self,
        driver: WebDriver,
        url: str = settings.SBIS_URL,
        timeout: int = 10,
    ):
        self.driver = driver
        self.url = url
        self.driver.implicitly_wait(timeout)
        self.driver.get(self.url)

    def element_clickable(self, element: tuple[str, str], timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(element),
            f"Элемент `{element}` не доступен!",
        ).click()

    def find_element(self, locator: tuple[str, str], timeout: int = 10) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator),
            f"Нет элемента {locator}!",
        )

    def find_elements(
        self, locator: tuple[str, str], timeout: int = 10
    ) -> list[WebElement]:
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator),
            f"Нет элементов {locator}!",
        )

    def find_element_and_clickable(self, element: tuple[str, str]) -> None:
        self.element_clickable(self.find_element(element))


class SbisContactsPage(BasePage):
    def click_tensor_banner(self) -> None:
        self.find_element_and_clickable(settings.TENSOR_BANNER)
        new_window = self.driver.window_handles[1]
        self.driver.switch_to.window(new_window)


class TensorPage(BasePage):
    def is_power_in_people_block(self) -> str:
        return self.find_element(settings.IS_POWER_IN_PEOPLE_BLOCK).text


class AboutPage(BasePage):
    @staticmethod
    def __get_image_dimensions(image_element: WebElement) -> tuple:
        image_size = image_element.size
        return (image_size["height"], image_size["width"])

    def are_images_dimensions_equal(self) -> bool:
        block_element = self.find_element(settings.BLOCK_IMAGE)
        image_elements = block_element.find_elements(*settings.TAG_IMAGE)
        dimensions_set = set()
        for image_element in image_elements:
            dimensions_set.add(self.__get_image_dimensions(image_element))

        return len(dimensions_set) == 1


class ContactsLocationPage(SbisContactsPage):
    def is_region_correct(self) -> str:
        return self.find_element(settings.REGION_NOW).text

    def change_region(self, region) -> None:
        self.find_element_and_clickable(settings.REGION_NOW)
        time.sleep(1)

        self.find_element_and_clickable((By.CSS_SELECTOR, f'[title="{region}"]'))
        time.sleep(1)


class DownloadPlugin(BasePage):
    @staticmethod
    def _extract_file_size(input_string) -> float | None:
        match = re.search(r"\d+\.\d+", input_string)
        return float(match.group()) if match else None

    @staticmethod
    def _get_file_size(file_path) -> float | None:
        return (
            round(os.path.getsize(file_path) / 1024 / 1024, 2)
            if os.path.isfile(file_path)
            else None
        )

    def open_footer_link(self) -> None:
        footer_link = self.find_element(settings.FOOTER_LINK_TEXT)
        self.driver.execute_script("arguments[0].click();", footer_link)

    def download_file(self, stated_size: int = 0) -> tuple[int, float | None, str]:
        sibs_plagin = self.find_elements(settings.LINK_SBIS_PLAGIN)
        time.sleep(1)

        for element in sibs_plagin:
            if settings.LINK_TEXT_SBIS_PLAGIN[1] in element.text:
                self.element_clickable(element)
                break

        sibs_plagin = self.find_elements(settings.LINK_DOWNLOAD)
        for element in sibs_plagin:
            if settings.LINK_DOWNLOAD_TEXT_SBIS_PLAGIN in element.text:
                element = element.find_element(*settings.LINK_TEXT_DOWNLOAD)
                stated_size = self._extract_file_size(element.text)
                self.driver.execute_script("arguments[0].click();", element)

                # Ждем, пока файл будет загружен
                while not any(
                    fname.startswith("sbis") for fname in os.listdir(settings.BASE_DIR)
                ):
                    time.sleep(1)

                break

        # Получаем имя скаченного файла
        filename = [
            fname for fname in os.listdir(settings.BASE_DIR) if fname.startswith("sbis")
        ][0]
        return stated_size, self._get_file_size(filename), filename
