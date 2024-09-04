from db import *
from utils import translate_origin 


def main():
    db = DataBase("sqlite:///data.db")
    session = db.get_session()

    horses = session.query(Horse).all()
    for horse in horses:
        horse.origin = translate_origin(horse.origin)
    
    session.commit()


if __name__ == "__main__":
    main()
