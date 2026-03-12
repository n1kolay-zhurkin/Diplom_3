import pytest
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.login_page import LoginPage
from utils.urls import Urls
from utils.data import TestData


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser: chrome or firefox")


@pytest.fixture
def driver(request):
    browser_name = request.config.getoption("--browser")

    if browser_name == "chrome":
        chromedriver_autoinstaller.install()
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)

    elif browser_name == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)
        driver.maximize_window()

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    yield driver
    driver.quit()


@pytest.fixture
def logged_in_user(driver):
    """Фикстура для авторизованного пользователя"""
    main_page = MainPage(driver)
    login_page = LoginPage(driver)
    
    # Переход на страницу логина
    driver.get(Urls.LOGIN)

    # Логин
    login_page.login(TestData.USER_EMAIL, TestData.USER_PASSWORD)

    # После логина возвращаемся на главную
    driver.get(Urls.BASE)
    
    # Переход в ленту заказов
    main_page.click_order_feed()
    feed_page = OrderFeedPage(driver)

    return main_page, feed_page