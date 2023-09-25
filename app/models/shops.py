from tortoise import fields, BaseDBAsyncClient
from tortoise.expressions import Q
from tortoise.queryset import QuerySet

from typing import Optional, Any
from datetime import time

from .locations import Street
from .base import TortoiseModel


class Shop(TortoiseModel):
    """Shop entity model."""
    name = fields.CharField(max_length=255)
    city = fields.ForeignKeyField("models.City")
    street = fields.ForeignKeyField("models.Street")
    time_open = fields.TimeField()
    time_close = fields.TimeField()

    @classmethod
    async def create(
        cls,
        name: str,
        city_id: str,
        street_id: str,
        time_open: time,
        time_close: time,
        using_db: Optional[BaseDBAsyncClient] = None,
    ) -> Optional["Shop"]:
        street = await Street.get_or_none(id=street_id)
        if street is None:
            return None
        return await (  # type: ignore
            super()
            .create(
                name=name,
                city_id=city_id,
                street=street,
                time_open=time_open,
                time_close=time_close,
                using_db=using_db
            )
        )


    @classmethod
    def filter(cls, *args: Q, **kwargs: Any) -> QuerySet["Shop"]:
        return (    # type: ignore
            super()
            .filter(*args, **kwargs)
            .select_related("shop", "city")
        )

    def __str__(self) -> str:
        return self.name
