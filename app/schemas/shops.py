from pydantic import BaseModel
from datetime import time


class BaseShopScheme(BaseModel):
    name: str
    time_open: time
    time_close: time


class ShopCreateScheme(BaseShopScheme):
    city_id: str
    street_id: str


class ShopCreateResponseScheme(BaseModel):
    id: str


class ShopListScheme(BaseShopScheme):
    id: str
    city_name: str
    street_name: str
