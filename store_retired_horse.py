from reader import DataReader
from db import DataBase


def get_all_urls(path="logs/build_db.log"):
    urls = set()
    f = open(path, "r", newline="")
    
    for line in f:
        url = line.split("url=")[-1]
        urls.add(url)

    f.close()
    return urls


def main():
    reader = DataReader()
    db = DataBase("sqlite:///data.db")

    urls = get_all_urls()
    for url in urls:
        horse = reader.read_retired_horse(url)
        db.store_horse(horse)


if __name__ == "__main__":
    main()