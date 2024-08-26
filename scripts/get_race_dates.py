from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from datetime import datetime, timedelta
import csv
from tqdm import tqdm


race_url = "https://racing.hkjc.com/racing/information/Chinese/Racing/LocalResults.aspx?"


def race_url_from_date_number(race_date):
    date_str = datetime.strftime(race_date, "%d/%m/%Y")
    url = race_url + "RaceDate=" + date_str
    return url


def is_race(driver: webdriver.Chrome, url):
    driver.get(url)
    try:
        driver.find_element(By.CLASS_NAME, "race_tab")
        return True
    except NoSuchElementException:
        return False


def max_race_number(driver: webdriver.Chrome, url):
    driver.get(url)
    race_count_row = driver.find_element(By.CLASS_NAME, "js_racecard").find_element(By.CSS_SELECTOR, "tr")
    race_count = len(race_count_row.find_elements(By.CSS_SELECTOR, "img")) - 1
    
    return race_count


def get_all_dates(writer: csv.writer, driver: webdriver.Chrome, start_date=datetime(2022,9,1).date(), days=365):
    for i in tqdm(range(days), desc="Reading race dates"):
        date = start_date + timedelta(days=i)
        url  = race_url_from_date_number(date)
        if is_race(driver, url):
            max_num = max_race_number(driver, url)
            writer.writerow([date.year, date.month, date.day, max_num])


def main():
    file = open("race_dates.csv", "w", newline="")
    writer = csv.writer(file, delimiter=",")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    
    get_all_dates(writer, driver, days=730)
    file.close()


if __name__ == "__main__":
    main()
