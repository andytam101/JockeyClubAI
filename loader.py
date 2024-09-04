import numpy as np
from tqdm import tqdm

from db import *
from horse_queries import get_horse_data, get_trainer_stats
from race_queries import get_race_data
from participation_queries import get_participation_data, get_group_participation_speed, get_rider_stats


class DataLoader: 
    def __init__(self, db: DataBase):
        self.db = db
        self.trainer_stats = get_trainer_stats(self.db)
        self.rider_stats   = get_rider_stats(self.db)

    def load_all_data(self):
        ps = self.db.get_all_participations()
        data = []
        times = []

        for p in tqdm(ps, desc="Loading data"):
            data.append(self.load_participation(p))
            times.append(float(p.finalTime))

        return np.array(data), np.array(times, dtype=np.float32)


    def load_participation(self, p: Participation):
        # an optimization can be to calculate everything in init so only perform lookup in this function (except participation_arr)
        season  = p.season
        raceId  = p.raceId
        horseId = p.horseId
        
        horse = self.db.get_horse(horseId) # TODO: missing fur colour
        race  = self.db.get_race(season=season, raceId=raceId)

        # add filter to get rid of "future" races
        participations = self.db.get_all_participations_for_horse(horseId)
        distances      = map(self.db.get_distance_of_participation, participations)

        if horse is not None:
            horse_arr     = get_horse_data(horse)
            trainer_arr   = self.trainer_stats[horse.trainer]
        else:
            horse_arr     = np.zeros(11, dtype=np.float32)
            trainer_arr   = np.zeros(10, dtype=np.float32)
        race_arr          = get_race_data(race)
        participation_arr = get_participation_data(p)
        rider_arr         = self.rider_stats[p.rider]
        time_arr          = get_group_participation_speed(zip(participations, distances))
        # TODO: missing equipment

        return np.concat((
            horse_arr,          # 0 - 10
            trainer_arr,        # 11 - 20
            race_arr,           # 21 - 26
            participation_arr,  # 27 - 29
            rider_arr,          # 30 - 41
            time_arr            # 42 - 53
        ))

def main():
    db     = DataBase("sqlite:///data.db")
    print("Preparing data loader...")
    loader = DataLoader(db)
    data, times = loader.load_all_data()
    np.save("data.npy", data)    
    np.save("times.npy", times)


if __name__ == "__main__":
    db = DataBase("sqlite:///data.db")
    p = db.get_all_participations()[0]
    loader = DataLoader(db)
    loader.load_participation(p)
