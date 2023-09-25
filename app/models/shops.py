from tortoise import fields, BaseDBAsyncClient
from tortoise.expressions import Q

from typing import Optional, Any
from datetime import time, datetime

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
        """Create custom method to get street and city if exists."""
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
    async def filter(cls, *args: Q, **kwargs: Any) -> list["Shop"]:
        """Filter method db optimizing."""
        return await (
            super()
            .filter(*args, **kwargs)
            .select_related("street", "city")
        )

    @classmethod
    async def all(cls, using_db: Optional[BaseDBAsyncClient] = None) -> list["Shop"]:
        """All method db optimizing."""
        return await (
            super()
            .all(using_db=using_db)
            .select_related("street", "city")
        )

    @classmethod
    async def filter_shops(
            cls,
            city_name: str | None,
            street_name: str | None,
            open_: bool | None
    ) -> list["Shop"]:
        """Custom filter method for getting shop list."""
        where = {}  # filter expressions dict
        if city_name is not None:
            where["city__name"] = city_name
        if street_name is not None:
            where['street__name'] = street_name
        if open_ is not None:
            now_time = datetime.now().time()
            if open_:
                where["time_open__gte"] = now_time
                where["time_close__lt"] = now_time
            else:
                where["time_open__lt"] = now_time
                where["time_close__gte"] = now_time
        if where == {}:
            return await cls.all()  # type: ignore
        return await cls.filter(**where)

    def __str__(self) -> str:
        return self.name
