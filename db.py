from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum, Boolean, ForeignKey, Time, DECIMAL, Date
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()


class Horse(Base):
    __tablename__ = "horse"

    horseId        = Column(String, primary_key=True)
    name           = Column(String, nullable=True)
    age            = Column(String)
    gender         = Column(String)
    furColour      = Column(String)
    origin         = Column(String)
    importType     = Column(String)
    currentRating  = Column(Integer, nullable=True)
    startingRating = Column(Integer, nullable=True)
    goldCount      = Column(Integer)
    silverCount    = Column(Integer)
    bronzeCount    = Column(Integer)
    totalEntries   = Column(Integer)
    seasonPrize    = Column(Integer)
    totalPrize     = Column(Integer)
    trainer        = Column(String, nullable=True)
    url            = Column(String, unique=True)


class Race(Base):
    __tablename__ = "race"

    season      = Column(Integer, primary_key=True)
    raceId      = Column(Integer, primary_key=True)
    date        = Column(Date)
    classNo     = Column(Integer)
    location    = Column(Enum("ST", "HV"))
    racetrack   = Column(String)
    distance    = Column(Integer)
    situation   = Column(String)
    highQuality = Column(Boolean, default=False)
    fair        = Column(Enum("fair", "quick", "catch"), default="fair")  # quick = 快放，catch = 後上
    url         = Column(String, unique=True)


class Participation(Base):
    __tablename__ = "participation"

    season        = Column(Integer, ForeignKey("race.season", ondelete="CASCADE"), primary_key=True)    
    raceId        = Column(Integer, ForeignKey("race.raceId", ondelete="CASCADE"), primary_key=True)
    horseId       = Column(String, ForeignKey("horse.horseId", ondelete="CASCADE"), primary_key=True)
    finalTime     = Column(DECIMAL(precision=5, scale=2))
    ranking       = Column(Integer)
    rating        = Column(Integer, nullable=True)
    carriedWeight = Column(Integer)
    horseWeight   = Column(Integer)
    rider         = Column(String)
    lane          = Column(Integer)
    p1Time        = Column(DECIMAL(precision=4, scale=2))
    p2Time        = Column(DECIMAL(precision=4, scale=2))
    p3Time        = Column(DECIMAL(precision=4, scale=2))
    p4Time        = Column(DECIMAL(precision=4, scale=2), nullable=True)
    p5Time        = Column(DECIMAL(precision=4, scale=2), nullable=True)
    p6Time        = Column(DECIMAL(precision=4, scale=2), nullable=True)
    penFirst      = Column(DECIMAL(precision=4, scale=2))
    penSecond     = Column(DECIMAL(precision=4, scale=2))
    finalFirst    = Column(DECIMAL(precision=4, scale=2))
    finalSecond   = Column(DECIMAL(precision=4, scale=2))
    equipment     = Column(String, default="")


class DataBase:
    def __init__(self, db_path):
        self._engine = create_engine(db_path)
        Base.metadata.create_all(self._engine)

    def get_session(self):
        session = sessionmaker(bind=self._engine)
        return session()
    
    def horse_exist(self, horseId):
        try:
            session = self.get_session()
            return session.query(Horse).filter(Horse.horseId == horseId).first() is not None
        finally:
            session.close()

    def get_horse(self, horseId):
        try:
            session = self.get_session()
            return session.query(Horse).filter(Horse.horseId == horseId).first()
        finally:
            session.close()

    def get_horse_url(self, horseId):
        try: 
            session = self.get_session()
            return session.query(Horse).filter(Horse.horseId == horseId).first().url
        finally:
            session.close()

    def race_exist(self, season, raceId):
        try: 
            session = self.get_session()
            return session.query(Race).filter(Race.raceId == raceId).filter(Race.season == season).first() is not None
        finally:
            session.close()

    def get_race(self, season, raceId):
        try:
            session = self.get_session()
            return session.query(Race).filter(Race.raceId == raceId).filter(Race.season == season).first()
        finally:
            session.close()

    def ran_exist(self, season, raceId, horseId):
        try:
            session = self.get_session()
            return session.query(Participation).filter(Participation.raceId == raceId).filter(Participation.season == season).filter(Participation.horseId == horseId).first() is not None
        finally:
            session.close()

    def get_ran(self, season, raceId, horseId):
        try:
            session = self.get_session()
            return session.query(Participation).filter(Participation.raceId == raceId).filter(Participation.season == season).filter(Participation.horseId == horseId).first()
        finally:
            session.close()

    def get_all_horses(self):
        try:
            session = self.get_session()
            return session.query(Horse).all()   
        finally:
            session.close()

    def get_all_races(self):
        try:
            session = self.get_session()
            return session.query(Race).all()
        finally:
            session.close()

    def store_horse(self, horse_data):
        # updates horse if horse already exist, otherwise create one
        session = self.get_session()
        horseId = horse_data["horseId"]
        if self.horse_exist(horseId):
            # update
            horse = self.get_horse(horseId)
            horse.name=horse_data["name"]
            horse.age=horse_data["age"]
            horse.gender=horse_data["gender"]
            horse.furColour=horse_data["furColour"]
            horse.origin=horse_data["origin"]
            horse.importType=horse_data["importType"]
            horse.currentRating=horse_data["currentRating"]
            horse.startingRating=horse_data["startingRating"]
            horse.goldCount=horse_data["goldCount"]
            horse.silverCount=horse_data["silverCount"]
            horse.bronzeCount=horse_data["bronzeCount"]
            horse.totalEntries=horse_data["totalEntries"]
            horse.seasonPrize=horse_data["seasonPrize"]
            horse.totalPrize=horse_data["totalPrize"]
            horse.trainer=horse_data["trainer"]
            horse.url=horse_data["url"],
            
            session.commit()
        else:
            # create
            new_horse = Horse(
                horseId=horseId,
                name=horse_data["name"],
                age=horse_data["age"],
                gender=horse_data["gender"],
                furColour=horse_data["furColour"],
                origin=horse_data["origin"],
                importType=horse_data["importType"],
                currentRating=horse_data["currentRating"],
                startingRating=horse_data["startingRating"],
                goldCount=horse_data["goldCount"],
                silverCount=horse_data["silverCount"],
                bronzeCount=horse_data["bronzeCount"],
                totalEntries=horse_data["totalEntries"],
                seasonPrize=horse_data["seasonPrize"],
                totalPrize=horse_data["totalPrize"],
                trainer=horse_data["trainer"],
                url=horse_data["url"],
            )
            session.add(new_horse)
            session.commit()


    def store_race(self, race_data):
        # there should be no need to update race as it will never change
        session = self.get_session()
        season = race_data["season"]
        raceId = race_data["raceId"]

        if self.race_exist(raceId=raceId, season=season):
            # update race
            race = self.get_race(season, raceId)
            race.date=race_data["date"],
            race.classNo=race_data['classNo'],
            race.location=race_data["location"],
            race.racetrack=race_data["racetrack"],
            race.distance=race_data["distance"],
            race.situation=race_data["situation"],
            
            race.url=race_data["url"]
            session.commit()
        else:
            # create race
            new_race = Race(
                season=season,
                raceId=raceId,
                date=race_data["date"],
                classNo=race_data['classNo'],
                location=race_data["location"],
                racetrack=race_data["racetrack"],
                distance=race_data["distance"],
                situation=race_data["situation"],
                url=race_data["url"]
            )
            session.add(new_race)
            session.commit()


    def store_participation(self, participation_data: dict):
        # there should be no need to update race as it will never change
        session = self.get_session()
        season  = participation_data["season"]
        raceId  = participation_data["raceId"]
        horseId = participation_data["horseId"]

        if self.ran_exist(raceId=raceId, horseId=horseId, season=season):
            # update
            ran = self.get_ran(raceId=raceId, horseId=horseId, season=season)
            ran.finalTime     = participation_data.get("finalTime"),
            ran.ranking       = participation_data.get("ranking"),
            ran.rating        = participation_data.get("rating"),
            ran.carriedWeight = participation_data.get("carriedWeight"),
            ran.horseWeight   = participation_data.get("horseWeight"),
            ran.rider         = participation_data.get("rider"),
            ran.lane          = participation_data.get("lane"),
            ran.p1Time        = participation_data.get("p1Time"),
            ran.p2Time        = participation_data.get("p2Time"),
            ran.p3Time        = participation_data.get("p3Time"),
            ran.p4Time        = participation_data.get("p4Time"),
            ran.p5Time        = participation_data.get("p5Time"),
            ran.p6Time        = participation_data.get("p6Time"),
            ran.penFirst      = participation_data.get("penFirst"),
            ran.penSecond     = participation_data.get("penSecond"),
            ran.finalFirst    = participation_data.get("finalFirst"),
            ran.finalSecond   = participation_data.get("finalSecond"),
            ran.equipment     = participation_data.get("equipment")
        
            session.commit()

        else:
            # create
            new_ran = Participation(
                season        = participation_data.get("season"),
                raceId        = participation_data.get("raceId"),
                horseId       = participation_data.get("horseId"),
                finalTime     = participation_data.get("finalTime"),
                ranking       = participation_data.get("ranking"),
                rating        = participation_data.get("rating"),
                carriedWeight = participation_data.get("carriedWeight"),
                horseWeight   = participation_data.get("horseWeight"),
                rider         = participation_data.get("rider"),
                lane          = participation_data.get("lane"),
                p1Time        = participation_data.get("p1Time"),
                p2Time        = participation_data.get("p2Time"),
                p3Time        = participation_data.get("p3Time"),
                p4Time        = participation_data.get("p4Time"),
                p5Time        = participation_data.get("p5Time"),
                p6Time        = participation_data.get("p6Time"),
                penFirst      = participation_data.get("penFirst"),
                penSecond     = participation_data.get("penSecond"),
                finalFirst    = participation_data.get("finalFirst"),
                finalSecond   = participation_data.get("finalSecond"),
                equipment     = participation_data.get("equipment"),
            )

            session.add(new_ran)
            session.commit()
