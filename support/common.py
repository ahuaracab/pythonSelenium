# from time import sleep
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_element(driver, by_locator):
    try:
        return WebDriverWait(driver, 10).until(EC.visibility_of_element_located(by_locator))
    except TimeoutException:
        print(f"Timed out waiting for element {by_locator} to be visible.")
        raise  # Volvemos a lanzar la excepción después de manejarla


def get_element_text(driver, by_locator):
    return get_element(driver, by_locator).text


def type_element(driver, by_locator, text):
    get_element(driver, by_locator).send_keys(text)


def click_element(driver, by_locator):
    get_element(driver, by_locator).click()


def is_element_visible(self, by_locator):
    return get_element(self.driver, by_locator).is_displayed()
