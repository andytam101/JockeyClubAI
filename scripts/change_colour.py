from db import *
from utils import translate_colour 


def main():
    db = DataBase("sqlite:///data.db")
    session = db.get_session()

    horses = session.query(Horse).all()
    for horse in horses:
        horse.furColour = translate_colour(horse.furColour)
    
    session.commit()


if __name__ == "__main__":
    main()
