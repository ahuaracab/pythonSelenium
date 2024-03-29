from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# This class is the parent of all pages
# It contains all the generic methods and utilities for all pages


def get_element(driver, by_locator):
    try:
        return WebDriverWait(driver, 10).until(EC.visibility_of_element_located(by_locator))
    except (TimeoutException, NoSuchElementException) as e:
        print(f"The element {by_locator} was not found in the page. Error: {e}")


class BasePage:
    # -- BasePage constructor -- #
    def __init__(self, driver):
        self.driver = driver

    # -- Page actions -- #
    def get_element(self, by_locator):
        return get_element(self.driver, by_locator)

    def get_element_text(self, by_locator):
        return get_element(self.driver, by_locator).text

    def type_element(self, by_locator, text):
        get_element(self.driver, by_locator).send_keys(text)

    def click_element(self, by_locator):
        get_element(self.driver, by_locator).click()

    def is_element_visible(self, by_locator):
        return get_element(self.driver, by_locator).is_displayed()