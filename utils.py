from datetime import time, datetime, date

from db import *

RACE_URL = "https://racing.hkjc.com/racing/information/Chinese/Racing/LocalResults.aspx?"
TIMINGS_URL = "https://racing.hkjc.com/racing/information/chinese/Racing/DisplaySectionalTime.aspx?"
SEASON_START_MONTH = 9


def date_to_season(race_date):
    season = race_date.year
    season_start_month = SEASON_START_MONTH
    if season_start_month <= race_date.month <= 12:
        season += 1
    return season


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

