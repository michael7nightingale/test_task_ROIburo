from fastapi import HTTPException

from app.models import City


async def get_city_dependency(city_id: str) -> City:
    city = await City.get_or_none(id=city_id)
    if city is None:
        raise HTTPException(
            detail=f"City with id={city_id} does not exist.",
            status_code=404
        )
    return city
