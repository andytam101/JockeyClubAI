from sqlalchemy import and_
import numpy as np
import matplotlib.pyplot as plt

from db import *


def get_participation_data(p: Participation):
    return np.array([
        p.rating,
        p.carriedWeight / 100,
        p.horseWeight / 1000,
    ], dtype=np.float32)


def get_rider_stats(db: DataBase):
    riders = db.get_all_riders()
    result = {}
    for r in riders:
        ps = db.get_all_participations_for_rider(r)
        ds = map(db.get_distance_of_participation, ps)
        result[r] = get_group_participation_speed(zip(ps, ds))
    return result
                

def get_group_participation_speed(ps: list[tuple[Participation, int]], groups = 6):
    group_arr = np.array(list(map(lambda x: transform_time(x[0], x[1], groups=groups), ps)), dtype=np.float32)
    return np.concat((np.mean(group_arr, axis=0), np.std(group_arr, axis=0)))


def transform_time(p: Participation, distance: int, groups=6):
    return distance / groups / group_time(split_time_into_60(p), groups) 


def group_time(time, groups=6):
    n = len(time) // groups
    indices = np.arange(0, len(time), n)
    return np.add.reduceat(time, indices)


def split_time_into_60(p: Participation):
    timing = [p.p1Time, p.p2Time, p.p3Time]
    if p.p4Time is not None:
        timing.append(p.p4Time)
    if p.p5Time is not None:
        timing.append(p.p5Time)
    if p.p6Time is not None:
        timing.append(p.p6Time)

    n = len(timing) 
    if p.finalFirst is None:
        timing = np.array(timing, dtype=np.float32)
        divided = n * timing / 60
        return np.repeat(divided, 60 / n)
    else:
        timing  = np.array(timing[:-2], dtype=np.float32)
        divided = n * timing / 60
        splits  = np.array([p.penFirst, p.penSecond, p.finalFirst, p.finalSecond], dtype=np.float32)
        splits  = n * splits / 30
        if n == 4:
            splits_repeated = np.array([splits[0]] * 7 + [splits[1]] * 8 + [splits[2]] * 7 + [splits[3]] * 8)
        else:
            splits_repeated = np.repeat(splits, 30 / n)
        return np.concat((np.repeat(divided, 60 / n), splits_repeated))


def get_all_participation_with_distance(db: DataBase, distance):
    session = db.get_session()
    result = (
        session.query(Participation)
        .join(Race, and_(Participation.season == Race.season, Participation.raceId == Race.raceId))
        .filter(Race.distance == distance)
        .all()
    )
    session.close()
    return result


def test(db: DataBase):
    distances = [1000, 1200, 1400, 1600, 1650, 1800, 2000, 2200, 2400]
    distance_participations = list(map(lambda x: get_all_participation_with_distance(db, x), distances))
    result = []
    for idx, p in enumerate(distance_participations):
        result.append(distances[idx] / 6 / np.array(list(map(transform_time, p))))
    
    line_1 = []
    line_2 = []
    line_3 = []
    line_4 = []
    line_5 = []
    line_6 = []

    for r in result:
        averages = np.mean(r, axis=0)
        line_1.append(float(averages[0]))
        line_2.append(float(averages[1]))
        line_3.append(float(averages[2]))
        line_4.append(float(averages[3]))
        line_5.append(float(averages[4]))
        line_6.append(float(averages[5]))

    plt.plot(distances, line_1, label=1)
    plt.plot(distances, line_2, label=2)
    plt.plot(distances, line_3, label=3)
    plt.plot(distances, line_4, label=4)
    plt.plot(distances, line_5, label=5)
    plt.plot(distances, line_6, label=6)
    plt.legend(loc='upper left')
    plt.show()


def test_2(db: DataBase):
    session = db.get_session()
    print(set(map(lambda x: x[0], session.query(Participation.rider).all())))


if __name__ == "__main__":
    db = DataBase("sqlite:///data.db")
    print(get_rider_stats(db))
