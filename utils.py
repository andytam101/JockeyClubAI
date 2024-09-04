from datetime import time, datetime, date


RACE_URL = "https://racing.hkjc.com/racing/information/Chinese/Racing/LocalResults.aspx?"
TIMINGS_URL = "https://racing.hkjc.com/racing/information/chinese/Racing/DisplaySectionalTime.aspx?"
SEASON_START_MONTH = 9


def date_to_season(race_date):
    season = race_date.year
    season_start_month = SEASON_START_MONTH
    if season_start_month <= race_date.month <= 12:
        season += 1
    return season


def translate_colour(colour: str):
    translation = {
        "棗": "Bay",
        "沙": "Sand",
        "栗": "Maroon",
        "灰": "Gray",
        "深棗": "Dark Bay",
        "棕": "Brown",
        "黑": "Black",
    }
    
    colours = colour.split("／")
    try:
        return " / ".join(map(lambda x: translation[x.strip()], colours))
    except KeyError:
        return colour


def translate_gender(gender):
    if gender == "雄":
        return "M"
    elif gender == "雌":
        return "F"
    elif gender == "閹":
        return "C"
    else:
        return gender
    

def translate_origin(origin):
    # origin is most likely a country
    if origin == "美國":
        return "USA"
    elif origin == "日本":
        return "Japan"
    elif origin == "意大利":
        return "Italy"
    elif origin == "德國":
        return "Germany"
    elif origin == "阿根廷":
        return "Argentina"
    elif origin == "紐西蘭":
        return "New Zealand"
    elif origin == "智利":
        return "Chile"
    elif origin == "澳洲":
        return "Australia"
    elif origin == "法國":
        return "France"
    elif origin == "英國":
        return "UK"
    elif origin == "南非":
        return "South Africa"
    elif origin == "巴西":
        return "Brazil"
    elif origin == "愛爾蘭":
        return "Ireland"
    else:
        return origin


def construct_race_url(race_date: date, number, location=None):
    race_url = RACE_URL
    if location is str:
        return race_url + f"RaceDate={race_date.strftime("%Y/%m/%d")}" + f"&Racecourse={location}" + f"&RaceNo={number}"
    else:   
        return race_url + f"RaceDate={race_date.strftime("%Y/%m/%d")}" + f"&RaceNo={number}"


def construct_timings_url(race_date: date, number):
    timings_url = TIMINGS_URL
    return timings_url + f"RaceDate={race_date.strftime("%d/%m/%Y")}" + f"&RaceNo={number}"


def to_seconds(racetime: time):
    return racetime.minute * 60 + racetime.second + racetime.microsecond * (10 ** -6)


def translate_location(x):
    if x == "沙田":
        return "ST"
    else:
        return "HV"


def translate_class(x):
    if x == "新馬賽":
        return 0
    elif x[1] in "一二三四五":
        return 6 - chinese_to_number(x[1])
    else:
        return 5


def chinese_to_number(x):
    try:
        result = {
            "一": 1,
            "二": 2,
            "三": 3,
            "四": 4,
            "五": 5
        }[x]
    except KeyError:
        result = 0
    finally:
        return result
