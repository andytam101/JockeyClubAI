from db import *
from utils import translate_gender 


def main():
    db = DataBase("sqlite:///data.db")
    session = db.get_session()

    horses = session.query(Horse).all()
    for horse in horses:
        horse.gender = translate_gender(horse.gender)
    
    session.commit()


if __name__ == "__main__":
    main()
