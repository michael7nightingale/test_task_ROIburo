from pydantic import BaseModel


class BaseStreetScheme(BaseModel):
    id: str
    name: str


class StreetListScheme(BaseStreetScheme):
    pass


class BaseCityScheme(BaseModel):
    id: str
    name: str


class CityListSchema(BaseCityScheme):
    pass


class CityStreetsScheme(BaseCityScheme):
    streets: list[StreetListScheme]
