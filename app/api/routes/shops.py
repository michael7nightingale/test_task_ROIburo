from fastapi import APIRouter, Query, Body, HTTPException

from app.schemas.shops import ShopCreateScheme, ShopCreateResponseScheme, ShopListScheme
from app.models import Shop


router = APIRouter(prefix="/shop")


@router.post("/", response_model=ShopCreateResponseScheme)
async def create_shop(shop_create_data: ShopCreateScheme = Body()):
    """Endpoint for creating shop. If success, returns its id."""
    new_shop = await Shop.create(**shop_create_data.model_dump())
    if new_shop is None:
        raise HTTPException(
            detail="Cannot match city and street ids!",
            status_code=400
        )
    return new_shop


@router.get("/", response_model=list[ShopListScheme])
async def get_shops(
        street: str | None = Query(default=None),
        city: str | None = Query(default=None),
        open_: bool | None = Query(default=None, alias="open")
):
    """
    Endpoint for getting shop list on filter in query parameters.
    If there are not any, returns all shops.
    """
    shops = await Shop.filter_shops(street_name=street, city_name=city, open_=open_)
    return [
        ShopListScheme(**shop.as_dict(), city_name=shop.city.name, street_name=shop.street.name)
        for shop in shops
    ]
