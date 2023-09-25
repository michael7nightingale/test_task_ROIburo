from app.models import City, Street, Shop


async def load_city_data() -> None:
    city_data = [
        {"id": 'f9f64e0d-b4cf-4b2a-bea5-24d61693781d', "name": "Екатеринбург"},
        {"id": 'bf2ddcdd-9b11-4ef9-bb35-6f9886e5b6bf', "name": "Тюмень"},
        {"id": 'bf2qpcdd-9b11-4ef8-bb35-6f9886e5b6bf', "name": "Москва"},
        {"id": 'bf2qpcdd-9b11-4ef8-bb35-6f9886e5b6bf', "name": "Минск"},
    ]
    await City.bulk_create(
        [
            City(**data) for data in city_data
        ],
        ignore_conflicts=True
    )


async def load_all_data() -> None:
    await load_city_data()
