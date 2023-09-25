from tortoise import fields, BaseDBAsyncClient
from tortoise.expressions import Q, F

from typing import Optional, Any
from datetime import time, datetime, timezone

from .locations import Street
from .base import TortoiseModel


class Shop(TortoiseModel):
    """Shop entity model."""
    name = fields.CharField(max_length=255)
    street = fields.ForeignKeyField("models.Street")
    time_open = fields.TimeField()
    time_close = fields.TimeField()

    @classmethod
    async def create(
            cls,
            name: str,
            city_name: str,
            street_name: str,
            time_open: time,
            time_close: time,
            using_db: Optional[BaseDBAsyncClient] = None,
    ) -> Optional["Shop"]:
        """Create custom method to get street and city if exists."""
        street = await Street.get_or_none(name=street_name, city__name=city_name)
        if street is None:
            return None
        return await (  # type: ignore
            super()
            .create(
                name=name,
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
            .select_related("street", "street__city")
        )

    @classmethod
    async def all(cls, using_db: Optional[BaseDBAsyncClient] = None) -> list["Shop"]:
        """All method db optimizing."""
        return await (
            super()
            .all(using_db=using_db)
            .select_related("street", "street__city")
        )

    @classmethod
    async def filter_shops(
            cls,
            city_name: str | None,
            street_name: str | None,
            open_: bool | None
    ) -> list["Shop"]:
        """Custom filter method for getting shop list."""
        where_kwargs = {}  # filter expressions dict
        where_args = []
        if city_name is not None:
            where_kwargs["city__name"] = city_name
        if street_name is not None:
            where_kwargs['street__name'] = street_name
        if open_ is not None:
            now_datetime = datetime.now(tz=timezone.utc)
            now_time = time(
                hour=now_datetime.hour + 5,
                minute=now_datetime.minute,
                second=now_datetime.second,
                tzinfo=timezone.utc
            )
            if open_:
                queryset = await cls.filter(
                    time_open__lte=F("time_close"),
                    time_open__lt=now_time,
                    time_close__gte=now_time,
                    **where_kwargs
                )
                queryset.extend(
                    await cls.filter(
                        Q(time_open__lt=now_time) | Q(time_close__gte=now_time),
                        time_open__gt=F("time_close"),
                        **where_kwargs
                    )
                )
                return queryset
            else:
                queryset = await cls.filter(
                    Q(time_open__gt=now_time) | Q(time_close__lte=now_time),
                    time_open__lte=F("time_close"),
                    **where_kwargs
                )
                queryset.extend(
                    await cls.filter(
                        Q(time_open__gt=now_time),
                        time_open__gt=F("time_close"),
                        time_close__lte=now_time,
                        **where_kwargs
                    )
                )
                return queryset
        else:
            if not any([where_args, where_kwargs]):
                return await cls.all()  # type: ignore
            return await cls.filter(*where_args, **where_kwargs)

    def __str__(self) -> str:
        return self.name
