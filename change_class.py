from db import *
from utils import translate_class


def main(db: DataBase):
    session = db.get_session()

    races = session.query(Race).all()
    for race in races:
        race.classNo = translate_class(race.classNo)

    session.commit()


if __name__ == "__main__":
    db = DataBase("sqlite:///backup.db")
    main(db)
