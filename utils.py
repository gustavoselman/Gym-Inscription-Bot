from selenium.webdriver.chrome.options import Options

def get_chrome_options(show_interface=True):
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--ignore-certificate-errors")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--disable-dev-shm-usage")
    if not show_interface:
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
    return options
