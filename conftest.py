import pytest
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser: chrome or firefox")

@pytest.fixture
def driver(request):
    browser_name = request.config.getoption("--browser")
    if browser_name == "chrome":
        try:
            driver_path = ChromeDriverManager().install()
            if not driver_path.lower().endswith('.exe'):
                import glob
                base_dir = os.path.dirname(driver_path)
                exe_files = glob.glob(os.path.join(base_dir, '*.exe'))
                if exe_files:
                    driver_path = exe_files[0]
                else:
                    driver_path = ChromeDriverManager().install()
        except Exception:
            driver_path = ChromeDriverManager().install()
        
        service = ChromeService(driver_path)
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=service, options=options)
    elif browser_name == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)
        driver.maximize_window()
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    
    yield driver
    driver.quit()