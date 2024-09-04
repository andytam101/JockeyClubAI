from datetime import datetime, timedelta
import csv
import logging

from utils import *
from reader import DataReader
from db import *


def add_race_to_index(file, date, number):
    with open(file, "a", newline="") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow([date.year, date.month, date.day, number])


def get_horse(reader: DataReader, db: DataBase, url):
    try:
        horse = reader.read_horse(url)
        if horse is not None:
            return db.store_horse(horse)
    except Exception as e:
        logging.error(f"Error getting horse: {e}. url={url}")


def get_race(reader: DataReader, db: DataBase, url):
    try:
        race = reader.read_race(url)
        if race is not None:
            return db.store_race(race)
    except Exception as e:
        logging.error(f"Error gettin race: {e}. url={url}")


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


def update_latest(reader: DataReader, db: DataBase):
    yesterday = datetime.now().date() - timedelta(days=1)
    first_url = construct_race_url(yesterday, 1)
    if not reader.is_race(first_url):
        return
    
    number = reader.max_race_number(first_url)
    
    # add to index of race dates
    add_race_to_index("race_dates.csv", yesterday, number)
    
    for i in range(1, number + 1):
        race = get_race(reader, db, construct_race_url(yesterday, i))
        if race is not None:
            get_all_participations_for_race(reader, db, race)


def main():
    reader = DataReader()
    db = DataBase()

    update_latest(reader, db)


if __name__ == "__main__":
    main()
    