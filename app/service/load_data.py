from app.models import City, Street, Shop
import csv


def load_csv_data(filepath: str) -> list[dict]:
    with open(filepath) as file:
        return list(csv.DictReader(file))


async def load_city_data() -> None:
    city_data = load_csv_data("app/data/cities.csv")
    await City.bulk_create(
        [
            City(**data) for data in city_data
        ],
        ignore_conflicts=True
    )


async def load_street_data() -> None:
    street_data = load_csv_data("app/data/streets.csv")
    await Street.bulk_create(
        [
            Street(**data) for data in street_data
        ],
        ignore_conflicts=True
    )


async def load_all_data() -> None:
    await load_city_data()
    await load_street_data()
