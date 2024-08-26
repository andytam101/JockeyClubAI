from db import *
from reader import DataReader
from utils import *

import csv
from datetime import datetime
from tqdm import tqdm
import logging


def get_all_dates(dates_path):
    all_dates = []
    with open(dates_path, "r", newline="") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            year, month, day, count = map(int, row)
            date = datetime(year, month, day).date()
            all_dates.append((date, count))

    return all_dates


def get_horse(reader: DataReader, db: DataBase, url):
    try:
        horse = reader.read_horse(url)
        if horse is not None:
            db.store_horse(horse)
    except Exception as e:
        logging.error(f"Error getting horse: {e}. url={url}")
    

def get_all_horses(reader: DataReader, db: DataBase, location="HK"):
    horses_urls = reader.read_all_horses_url(location=location)
    for i in tqdm(range(len(horses_urls)), desc="Reading horses"):
        url = horses_urls[i]
        get_horse(reader, db, url)


def get_race(reader: DataReader, db: DataBase, url):
    try:
        race = reader.read_race_from_url(url)
        if race is not None:
            db.store_race(race)
    except Exception as e:
        logging.error(f"Error gettin race: {e}. url={url}")
        

def get_all_races(reader: DataReader, db: DataBase, start=0):
    dates = get_all_dates("race_dates.csv")[start:]
    for i in tqdm(range(len(dates)), desc="Reading races"):
        d, n = dates[i]
        
        # update reading object
        for i in range(1, n+1):
            url = construct_race_url(d, i)
            get_race(reader, db, url)            


def get_all_participations_for_race(reader: DataReader, db: DataBase, race: Race):
    url = race.url
    assert url[-8:-1] == "RaceNo="
    number = int(url[-1])
    
    # get participation data for all horses
    participations: list[dict] = reader.read_participation_of_race(url)
    timings_url = construct_timings_url(race.date, number)
    timings     = reader.read_timings_of_race(timings_url)

    for p in participations:
        try:
            horseId = p["horseId"]
            horse_url = p["horseURL"]

            # update horse if they do not exist
            if not db.horse_exist(horseId):
                get_horse(reader, db, horse_url)
            
            # combine with timings data
            this_timings = timings[horseId]
            p.update(this_timings)

            # get rating and equipment for horse
            rating_equipment = reader.read_rating_equipment(horse_url, race.raceId, race.season)
            p.update(rating_equipment)

            # store result
            db.store_participation(p)

        except Exception as e:
            logging.error(f"Error getting horse {horseId} participations in raceId={race.raceId}, season={race.season}: {e}. url={url}")


def get_all_participations(reader: DataReader, db: DataBase):
    races = db.get_all_races()
    for i in tqdm(range(len(races)), desc="Reading participations"):
        get_all_participations_for_race(reader, db, races[i])


def main(start=0):
    logging.basicConfig(filename="logs/build_db.log", level=logging.INFO)
    
    print("Preparing database...")
    db = DataBase(db_path="sqlite:///data.db")
    reader = DataReader()

    print("Reading data...")
    get_all_horses(reader, db, location="HK")
    get_all_horses(reader, db, location="CH")
    get_all_races(reader, db, start=start)
    get_all_participations(reader, db)


if __name__ == "__main__":
    main()
