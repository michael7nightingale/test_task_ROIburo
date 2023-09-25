from fastapi import APIRouter, Query, Body, HTTPException

from app.schemas.shops import ShopCreateScheme, ShopCreateResponseScheme
from app.models import Shop

router = APIRouter(prefix="")


@router.post("/shop", response_model=ShopCreateResponseScheme)
async def create_shop(shop_create_data: ShopCreateScheme = Body()):
    new_shop = await Shop.create(**shop_create_data.model_dump())
    if new_shop is None:
        raise HTTPException(
            detail="Cannot match city and street ids!",
            status_code=400
        )
    return new_shop
