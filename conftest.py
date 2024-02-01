import os
import time

import pytest

from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions

from datetime import datetime


@pytest.fixture(scope="class")
def base_url():
    return os.environ.get('BASE_URL')


@pytest.fixture(scope="class")
def username():
    return os.environ.get('USERNAME')


@pytest.fixture(scope="class")
def password():
    return os.environ.get('PASSWORD')


BUILD_ID = int(time.time())


@pytest.fixture(scope="class", params=["chrome", "edge"])
def driver(request):
    browser = request.param

    if os.environ.get("IS_LOCAL") == "True":

        if browser == 'edge':
            s = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=s)
        else:
            s = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=s)

    else:
        # BlazeMeter access configuration
        api_key = os.environ.get("API_KEY")
        api_secret = os.environ.get("API_SECRET")
        base = "a.blazemeter.com"
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        if browser == 'edge':
            browser = 'MicrosoftEdge'
            options = EdgeOptions()
        else:
            options = ChromeOptions()

        # BlazeMeter capabilities

        cloud_options = {
            'browserName': browser,
            'blazemeter.buildId': BUILD_ID,
            'blazemeter.testName': "Selenium Course Test",
            'blazemeter.reportName': f'{request.node.name}_{now}_{browser}'
        }
        options.set_capability('cloud:options', cloud_options)

        blazegrid_url = f'https://{api_key}:{api_secret}@{base}/api/v4/grid/wd/hub'
        driver = webdriver.Remote(blazegrid_url, options=options)

    driver.maximize_window()
    request.cls.driver = driver
    yield driver
    driver.close()
    driver.quit()


@pytest.mark.usefixtures("driver")
@pytest.fixture(scope="function", autouse=True)
def name_blazemeter_report(request, driver):
    args = {
        'testCaseName': request.node.name,
        'testSuiteName': request.node.parent.parent.name
    }

    driver.execute_script("/* FLOW_MARKER test-case-start */", args)

    yield

    if request.node.rep_setup.failed:
        # message = request.node.rep_setup.longrepr.repcrach.message
        message = 'broken'
        status = 'broken'

    elif request.node.rep_call.failed:
        # message = request.node.rep_setup.longrepr.repcrach.message
        message = 'failed'
        # is_assertion = 'AssertionError' in request.node.longreprtext
        # status = 'failed' if is_assertion else 'broken'
        status = 'failed'

    else:
        message = ''
        status = 'passed'

    args = {
        'message': message,
        'status': status
    }

    driver.execute_script("/* FLOW_MARKER test-case-stop */", args)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
