from datetime import time

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


class BaseShopScheme(BaseModel):
    name: str
    time_open: time
    time_close: time


class ShopCreateScheme(BaseShopScheme):
    city_id: str
    street_id: str


class ShopDetailScheme(BaseShopScheme):
    id: str
    city_name: str
    street_name: str
