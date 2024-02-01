from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from support.common import get_element, get_element_text, type_element, click_element

import pytest


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.close()
    driver.quit()


def test_login(driver):
    driver.get("http://dbankdemo.com/bank/login")

    assert 'Digital Bank' == driver.title

    type_element(driver, (By.ID, "username"), 'jsmith@demo.io')
    type_element(driver, (By.ID, "password"), 'Demo123!')
    click_element(driver, (By.ID, "submit"))

    assert 'home' in driver.current_url


def test_verify_version(driver):
    # driver.find_element(By.ID, 'aboutLink').click()
    # sleep(1)
    # assert '2.1.0.11' in driver.find_element(By.CLASS_NAME, 'modal-body').text
    get_element(driver, (By.ID, 'aboutLink')).click()

    assert '2.1.0.11' in get_element_text(driver, (By.CLASS_NAME, 'modal-body'))
