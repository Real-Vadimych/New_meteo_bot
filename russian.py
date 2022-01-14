import os
import re
import time

from dotenv import load_dotenv
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import settings
from splitter import cutter

load_dotenv()

def set_driver():
    ua = UserAgent()
    # ua.update()
    options = webdriver.ChromeOptions()
    # uncomment next rows after deploy on server
    options.add_argument(f"user-agent = {ua.chrome}")
    # options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(
        # switch next rows after deploy on server
        executable_path=settings.win_path,
        # executable_path=settings.linux_path,
        options=options,
    )


def connect_to_site(url: str, url2: str, r_type: str, airport: str):
    driver = set_driver()
    reques_dict = {"METAR": "SA", "TAF": "FT FC", "FA": "FA"}
    try:
        driver.get(url=url)
        time.sleep(2)
        login = os.getenv("LOGIN")
        password = os.getenv("PASSWORD")
        fill_the_field(driver, "login", login)
        fill_the_field(driver, "pass", password)
        driver.find_element(By.CSS_SELECTOR, 'input[type="image" i]').click()
        driver.get(url=url2)
        time.sleep(2)
        weather_request = driver.find_element(By.NAME, "bamdquery")
        weather_request.clear()
        r_type = reques_dict[r_type].upper()
        airport = airport.upper()
        request_text = f"{r_type} {airport}"
        weather_request.send_keys(request_text)
        driver.find_element_by_id("bamd").click()
        time.sleep(2)
        return driver.find_element_by_id("msg").text
    except Exception as ex:
        print(ex)
        driver.get(url=url)
        time.sleep(2)
    finally:
        driver.close()
        driver.quit()


def fill_the_field(driver, name, input_text):
    user_input = driver.find_element(By.NAME, name)
    user_input.clear()
    user_input.send_keys(input_text)


def get_weather(r_type: str, airport: str) -> str:
    url = "http://meteoinfo.gamc.ru/"
    url2 = "http://meteoinfo.gamc.ru/meteo_query"
    weather_text = connect_to_site(url=url, url2=url2, r_type=r_type, airport=airport)
    p = re.compile("(?s)-{40}(.*?)=", flags=re.DOTALL)
    answer = p.findall(weather_text)[0].replace("\n", "", 1)
    return split_message(answer)


def split_message(text: str) -> str:
    weather_text = ""
    if len(text) >= 2000:
        splitted_answer = cutter(text)
        for answers in splitted_answer:
            weather_text += answers
    else:
        weather_text = text

    return weather_text


if __name__ == "__main__":
    get_weather()
