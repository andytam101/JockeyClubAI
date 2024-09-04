from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from datetime import datetime
import logging

from utils import *

class DataReader:
    def __init__(
            self, 
            base_url="https://racing.hkjc.com",
            all_horses_url="https://racing.hkjc.com/racing/information/chinese/Horse/ListByLocation.aspx?Location=",
            race_url="https://racing.hkjc.com/racing/information/Chinese/Racing/LocalResults.aspx?",
            sectional_time_url="https://racing.hkjc.com/racing/information/chinese/Racing/DisplaySectionalTime.aspx?",
            season_start_month = 9
        ) -> None:        

        chromedriver_path = "/home/andytam321/anaconda3/envs/JockeyClub/lib/python3.12/site-packages/chromedriver_autoinstaller/127/chromedriver"
        service = webdriver.ChromeService(chromedriver_path)

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=service, options=options)
        
        self.base_url = base_url
        self.all_horses_url = all_horses_url
        self.race_url = race_url
        self.sectional_time_url = sectional_time_url
        self.season_start_month = season_start_month
    
    def is_race(self, url):
        self.driver.get(url)
        try:
            self.driver.find_element(By.CLASS_NAME, "race_tab")
            return True
        except NoSuchElementException:
            return False
        
    def max_race_number(self, url):
        self.driver.get(url)
        race_count_row = self.driver.find_element(By.CLASS_NAME, "js_racecard").find_element(By.CSS_SELECTOR, "tr")
        race_count = len(race_count_row.find_elements(By.CSS_SELECTOR, "img")) - 1
        
        return race_count
        
    def read_all_horses_url(self, location="HK"):
        def get_link(element: WebElement):
            return element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

        self.driver.get(self.all_horses_url + location)
        horses = self.driver.find_elements(By.CLASS_NAME, "bigborder")[1].find_element(By.CSS_SELECTOR, "table")
        all_horses = horses.find_elements(By.CLASS_NAME, "table_text_two")[0:-1:2]

        return list(map(get_link, all_horses))

    def read_horse(self, url):
        """read horse profile page"""

        def extract_third_td(element: WebElement):
            return element.find_elements(By.CSS_SELECTOR, "td")[2].text

        self.driver.get(url)

        horse_details = self.driver.find_element(By.CLASS_NAME, "title_text").text.split(" ")
        try:
            name, horseId = horse_details
        except ValueError:
            # retired horse
            return self.read_retired_horse(url)

        if name == "未命名":
            name = None

        horseId = horseId[1:-1]  # get rid of surrounding brackets

        left, right = self.driver.find_elements(By.CLASS_NAME, "table_top_right")

        data = list(map(extract_third_td, left.find_elements(By.CSS_SELECTOR, "tr")))   
        
        origin_age = data[0].split(" / ")
        origin = translate_origin(origin_age[0])
        try:
            age = origin_age[1]
            age = int(age)
        except IndexError:
            # retired horse
            self.read_retired_horse(url)

        colour, gender = data[1].split(" / ")
        colour = translate_colour(colour)
        gender = translate_gender(gender)
        importType = data[2]
        try:
            seasonPrize = int(data[3][1:].replace(",", ""))
            totalPrize  = int(data[4][1:].replace(",", ""))
            gold, silver, bronze, entries = map(int, data[5].split("-"))
        except (ValueError, IndexError):
            return self.read_retired_horse(url)

        right_rows = right.find_elements(By.CSS_SELECTOR, "tr")
        data = list(map(extract_third_td, right_rows))

        if right_rows[0].find_element(By.CSS_SELECTOR, "td").text == "練馬師":
            trainer = data[0]
        else:
            trainer = None

        try:
            currentRating  = int(data[2])
        except:
            currentRating = None
        
        try:
            startingRating = int(data[3])
        except:
            startingRating = None        

        return {
            "horseId": horseId,
            "name": name,
            "age": age,
            "gender": gender,
            "furColour": colour,
            "origin": origin,
            "importType": importType,
            "currentRating": currentRating,
            "startingRating": startingRating,
            "goldCount": gold,
            "silverCount": silver,
            "bronzeCount": bronze,
            "totalEntries": entries,
            "seasonPrize": seasonPrize,
            "totalPrize": totalPrize,
            "trainer": trainer,
            "url": url,
        }
    
    def read_retired_horse(self, url):
        
        def extract_third_td(element: WebElement):
            return element.find_elements(By.CSS_SELECTOR, "td")[2].text
        
        self.driver.get(url)

        horse_details = self.driver.find_element(By.CLASS_NAME, "title_text").text.split(" ")
        name = horse_details[0]
        horseId = horse_details[1][1:-1]

        left, right = self.driver.find_elements(By.CLASS_NAME, "table_top_right")
        data = list(map(extract_third_td, left.find_elements(By.CSS_SELECTOR, "tr")))

        origin_age = data[0].split(" / ")
        origin = translate_origin(origin_age[0])
        try:
            age = int(origin_age[1])
        except (IndexError, ValueError):
            age = None

        colour, gender = data[1].split(" / ")
        colour = translate_colour(colour)
        gender = translate_gender(gender)
        importType = data[2]
        totalPrize  = int(data[3][1:].replace(",", ""))
        gold, silver, bronze, entries = map(int, data[4].split("-"))

        right_rows = right.find_elements(By.CSS_SELECTOR, "tr")
        data = list(map(extract_third_td, right_rows))

        try:
            currentRating = int(data[1])
        except ValueError:
            currentRating = None

        startingRating = currentRating

        return {
            "horseId": horseId,
            "name": name,
            "age": age, 
            "gender": gender,
            "furColour": colour,
            "origin": origin,
            "importType": importType,
            "currentRating": currentRating,
            "startingRating": startingRating,
            "goldCount": gold,
            "silverCount": silver,
            "bronzeCount": bronze,
            "totalEntries": entries,
            "totalPrize": totalPrize,
            "url": url,
        }

    def read_race(self, url):
        """read race page"""

        self.driver.get(url)
        meeting = self.driver.find_element(By.CLASS_NAME, "raceMeeting_select")
        table = self.driver.find_element(By.CLASS_NAME, "race_tab")

        details = meeting.find_element(By.CLASS_NAME, "f_fs13").text

        _, date, location = details.split()
        date = datetime.strptime(date, "%d/%m/%Y").date()
        season = date_to_season(date)

        location = translate_location(location)

        # get things in table first
        rows = table.find_elements(By.CSS_SELECTOR, "tr")
        raceId = int(rows[0].text.split(" (")[1][:-1])

        if raceId <= 0:
            # invalid race
            logging.info(f"Encountered invalid race. url={url}")
            return None

        row_2 = rows[2].find_elements(By.CSS_SELECTOR, "td")

        class_dist_row = row_2[0]
        row_text = class_dist_row.text.split(" - ")
        class_no, dist = row_text[0], row_text[1]

        dist = int(dist[:-1])

        situation = row_2[2].text

        if len(situation) == 0:
            # invalid race
            logging.info(f"Encountered invalid race. url={url}")
            return None

        racetrack = rows[3].find_elements(By.CSS_SELECTOR, "td")[2].text[:-2].strip()

        return {
            "season": season,
            "raceId": raceId,
            "date": date,
            "classNo": class_no,
            "location": location,
            "racetrack": racetrack,
            "distance": dist,
            "situation": situation,
            "url": url
        }    

    def read_timings_of_race(self, url):
        self.driver.get(url)
        horses = self.driver.find_element(By.CLASS_NAME, "race_table").find_element(
            By.CSS_SELECTOR, "tbody").find_elements(By.CSS_SELECTOR, "tr")
        
        result: dict[int, dict] = {}
        for h in horses:
            data = h.find_elements(By.CSS_SELECTOR, "td")
            horseId = data[2].text.split(" (")[1][:-1]
            try:
                int(data[0].text)
            except ValueError:
                # disqualified or left
                continue

            result.update({horseId: {}})

            counter = 1
            final = False
            timings = h.find_elements(By.CSS_SELECTOR, "td")[3:-1]
            for time in timings:
                if time.text == '':
                    break
                all_times = list(map(float, time.text.splitlines()[2].split()))
                section_time = all_times[0]
                if len(all_times) > 1:
                    if final:
                        result[horseId].update({"finalFirst": all_times[1]})
                        result[horseId].update({"finalSecond": all_times[2]})
                    else:
                        result[horseId].update({"penFirst": all_times[1]})
                        result[horseId].update({"penSecond": all_times[2]})
                        final = True

                result[horseId].update({f"p{counter}Time": section_time})
                counter += 1
        
        return result

    def read_participation_of_race(self, url):
        self.driver.get(url)

        date_str = self.driver.find_element(By.CSS_SELECTOR, ".f_fl.f_fs13").text.split()[1]
        season = date_to_season(datetime.strptime(date_str, "%d/%m/%Y"))
        raceId = self.driver.find_element(By.CSS_SELECTOR, ".bg_blue.color_w.font_wb").find_element(By.CSS_SELECTOR, "td").text.split()[-1][1:-1]

        table  = self.driver.find_element(By.CSS_SELECTOR, ".f_fs12.fontFam")
        result = [] 

        for row in table.find_elements(By.CSS_SELECTOR, "tr"):
            data = row.find_elements(By.CSS_SELECTOR, "td")
            try:
                try:
                    ranking = int(data[0].text)
                except ValueError:
                    # got disqualified or did not participate
                    continue
            
                horseId = data[2].text.split()[1][1:-1]
                horseURL = data[2].find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                rider = data[3].text
                carried_weight = int(data[5].text)
                horse_weight = int(data[6].text)
                lane = int(data[7].text)
                final_time = to_seconds(datetime.strptime(data[10].text, "%M:%S.%f").time())    

                result.append({
                    "season": season,
                    'raceId': raceId,
                    "horseId": horseId,
                    "horseURL": horseURL,
                    "finalTime": final_time,
                    "ranking": ranking,
                    "carriedWeight": carried_weight,
                    "horseWeight": horse_weight,
                    "rider": rider,
                    "lane": lane
                })
            except Exception as e:
                print(url)
                print(data)
                raise e

        return result
        
    def read_rating_equipment(self, url, raceId, season):
        self.driver.get(url)
        table = self.driver.find_element(By.CLASS_NAME, "bigborder")
       
        for row in table.find_elements(By.CSS_SELECTOR, "tr")[1:]:
            data = row.find_elements(By.CSS_SELECTOR, "td")
            if len(data) <= 1:
                continue
            
            try:
                raceId = int(data[0].text)
            except ValueError:
                # overseas
                continue

            try:
                season = date_to_season(datetime.strptime(data[2].text, "%d/%m/%y"))
            except ValueError:
                # retired horse
                season = date_to_season(datetime.strptime(data[2].text, "%d/%m/%Y"))
            
            if raceId != raceId or season != season:
                continue

            try:
                rating = int(data[8].text)
            except ValueError:
                rating = None

            equipment = data[17].text

            return {
                "rating": rating,
                "equipment": equipment,
            }


if __name__ == "__main__":
    dr = DataReader()
    print(dr.read_retired_horse("https://racing.hkjc.com/racing/information/Chinese/Horse/OtherHorse.aspx?HorseId=HK_2022_H138"))
    print(dr.read_retired_horse("https://racing.hkjc.com/racing/information/Chinese/Horse/Horse.aspx?HorseId=HK_2021_G235"))
    print(dr.read_retired_horse("https://racing.hkjc.com/racing/information/Chinese/Horse/Horse.aspx?HorseId=HK_2022_H823"))
