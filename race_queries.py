import numpy as np

from db import *
from utils import *


def get_race_data(race: Race):
    return np.concat((
        np.array([race.distance / 1000, translate_class(race.classNo)], dtype=np.float32),
        convert_situation(race.situation), 
        # location_array(race.location, race.racetrack)
    ))


def convert_situation(situation: str):
    # might need to change according to the data
    result = np.zeros(4, dtype=np.float32)
    
    convertion = {
        "快地": 1,
        "好地": 2,
        "黏地": 3,
        "軟地": 4,
        "大爛地": 5
    }

    if situation[0] == "濕":
        result[1] = 1
        result[3] = 1 if situation[1] == "快" else -1
    else:
        result[0] = 1
        result[2] = np.mean(list(map(lambda x: convertion[x], situation.split("至"))))

    return result


def location_array(location, racetrack):
    return np.array([
        location == "ST" and racetrack == '草地 - "A"',
        location == "ST" and racetrack == '草地 - "B"',
        location == "ST" and racetrack == '草地 - "C"',
        location == "ST" and racetrack == '草地 - "B+2"',
        location == "ST" and racetrack == '草地 - "C+3"',
        location == "ST" and racetrack == '草地 - "A+3"',
        location == "ST" and racetrack == '全天候',
        location == "HV" and racetrack == '草地 - "A"',
        location == "HV" and racetrack == '草地 - "B"',
        location == "HV" and racetrack == '草地 - "C"',
        location == "HV" and racetrack == '草地 - "B+2"',
        location == "HV" and racetrack == '草地 - "C+3"',
        location == "HV" and racetrack == '草地 - "A+3"',
        location == "HV" and racetrack == '全天候',
    ], dtype=np.float32)


def test(db: DataBase):
    races = db.get_all_races()
    print(set(map(lambda x: x.classNo, races)))
    print(set(map(lambda x: x.situation, races)))
    print(set(map(lambda x: x.racetrack, races)))
    print(set(map(lambda x: x.distance, races)))


if __name__ == "__main__":
    db = DataBase("sqlite:///data.db")
    test(db)
