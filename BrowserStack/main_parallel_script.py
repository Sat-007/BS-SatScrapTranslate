import threading
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from scripts.website_scrapper import search_automation
from scripts.translator import run_scrapper
from scripts.header_word_count import analyze_word_frequency


USERNAME = "sathvikkondur_KcHSNA"
ACCESS_KEY = "yYKTu9XR6szuq8TTs65G"

capabilities_list = [
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "10"
    },
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "os": "OS X",
        "osVersion": "Monterey"
    },
    {
        "deviceName": "PIXEL 9 PRO XL ",
        "realMobile": "true",
        "osVersion": "12.0",
        "browserName": "Android"
    },
    {
        "browserName": "Edge",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "11"
    }
]

def run_on_browserstack(capabilities):
    options = Options()
    for key, value in capabilities.items():
        options.set_capability(key, value)

    options.set_capability("browserstack.user", USERNAME)
    options.set_capability("browserstack.key", ACCESS_KEY)
    options.set_capability("project", "SatScrapTranslate")
    options.set_capability("name", f"Run on {capabilities.get('browserName', capabilities.get('deviceName'))}")

    driver = WebDriver(
        command_executor="https://hub-cloud.browserstack.com/wd/hub",
        options=options
    )

    try:
        articles = search_automation(driver)
        translated = run_scrapper(articles)
        frequency = analyze_word_frequency(translated)
        print(f"Result in  {capabilities.get('browserName', capabilities.get('deviceName'))}:\n{frequency}\n")
    except Exception as e:
        print(f" Error occured in {capabilities.get('browserName', capabilities.get('deviceName'))}: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    threads = []

    for caps in capabilities_list:
        thread = threading.Thread(target=run_on_browserstack, args=(caps,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()



