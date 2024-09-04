import numpy as np
import matplotlib.pyplot as plt

from db import *


def colour_to_grayscale():
    pass


def get_horse_data(horse: Horse):   
    return np.array([
        horse.age if horse.age is not None else 0,
        horse.gender == "M",
        horse.gender == "F",
        horse.gender == "C",

        # TODO: add fur colour

        horse.importType == "自購馬",
        horse.importType == "自購新馬",
        horse.importType == "國際拍賣會新馬",
        horse.goldCount / horse.totalEntries,
        horse.silverCount / horse.totalEntries,
        horse.bronzeCount / horse.totalEntries,
        horse.totalEntries,
    ], dtype=np.float32)


def get_horse_group_values(horses: list[Horse]):
    # useful stuff for trainer: average rating, average starting rating, total gold, total silver, total bronze, total participation, average total prize 
    
    currentRating  = np.array(list(map(lambda x: x.currentRating if x.currentRating is not None else 0, horses)))
    startingRating = np.array(list(map(lambda x: x.startingRating if x.startingRating is not None else 0, horses)))
    goldCount      = np.array(list(map(lambda x: x.goldCount if x.goldCount is not None else 0, horses)))
    silverCount    = np.array(list(map(lambda x: x.silverCount if x.silverCount is not None else 0, horses)))
    bronzeCount    = np.array(list(map(lambda x: x.bronzeCount if x.bronzeCount is not None else 0, horses)))
    totalEntries   = np.array(list(map(lambda x: x.totalEntries if x.totalEntries is not None else 0, horses)))
    totalPrize     = np.array(list(map(lambda x: x.totalPrize if x.totalPrize is not None else 0, horses)))

    averagePrize   = totalPrize / totalEntries
    averagePrize   = np.nan_to_num(averagePrize, nan=1)

    n = len(horses)
    return np.array([
        np.mean(currentRating),
        np.std(currentRating),
        np.mean(startingRating),
        np.std(startingRating),
        np.log(np.mean(averagePrize)),
        np.log(np.std(averagePrize)),
        np.sum(goldCount) / n,
        np.sum(silverCount) / n,
        np.sum(bronzeCount) / n,
        np.sum(totalEntries) / n,
    ], dtype=np.float32)


def get_trainer_stats(db: DataBase):
    trainer_horses = categorize_horses_by_trainer(db.get_all_horses())
    return dict(map(lambda x: (x, get_horse_group_values(trainer_horses[x])), trainer_horses))


def get_origin_stats(db: DataBase):
    origin_horses = categorize_horses_by_origin(db.get_all_horses())
    return dict(map(lambda x: (x, get_horse_group_values(origin_horses[x])), origin_horses))


def categorize_horses_by_trainer(horses: list[Horse]):
    trainer_horses = {}

    for h in horses:
        if h.trainer in trainer_horses:
            trainer_horses[h.trainer].append(h)
        else:
            trainer_horses[h.trainer] = [h]

    return trainer_horses


def categorize_horses_by_origin(horses: list[Horse]):
    origin_horses = {}
    for h in horses:
        if h.origin in origin_horses:
            origin_horses[h.origin].append(h)
        else:
            origin_horses[h.origin] = [h]
    
    return origin_horses


def test(db: DataBase): 
    horses = db.get_all_horses()
    # print(set(map(lambda x: x.gender, horses)))
    # print(set(map(lambda x: x.origin, horses)))
    print(set(map(lambda x: x.importType, horses)))
    # trainer_horses = categorize_horses_by_trainer(horses)
    # print(get_horse_group_values(trainer_horses["呂健威"]))
    # print(get_origin_stats(db))

if __name__ == "__main__":
    db = DataBase("sqlite:///data.db")
    test(db)
