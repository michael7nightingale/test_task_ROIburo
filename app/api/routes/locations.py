from fastapi import APIRouter, Depends

from app.api.dependencies.locations import get_city_dependency
from app.schemas.locations import CityListSchema, CityStreetsScheme
from app.models import City

router = APIRouter(prefix="")


@router.get("/city", response_model=list[CityListSchema])
async def get_cities():
    return await City.all()


@router.get("/city/{city_id}/street", response_model=CityStreetsScheme)
async def get_city_streets(city: City = Depends(get_city_dependency)):
    return city
