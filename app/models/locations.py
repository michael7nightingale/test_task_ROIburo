from tortoise import fields, BaseDBAsyncClient
from tortoise.expressions import Q
from tortoise.queryset import QuerySetSingle, QuerySet

from typing import Optional, Any

from .base import TortoiseModel


class City(TortoiseModel):
    """City entity model."""
    name = fields.CharField(unique=True, index=True, max_length=255)

    def __str__(self) -> str:
        return f"г. {self.name}"

    @classmethod
    def get_or_none(
        cls, *args: Q, using_db: Optional[BaseDBAsyncClient] = None, **kwargs: Any
    ) -> QuerySetSingle[Optional["City"]]:
        return (
            super()
            .get_or_none(*args, using_db=using_db, **kwargs)
            .prefetch_related("streets")
        )


class Street(TortoiseModel):
    """Street entity model."""
    name = fields.CharField(max_length=255)
    city = fields.ForeignKeyField("models.City", related_name="streets")

    def __str__(self) -> str:
        return f"ул. {self.name}"

    class Meta:
        unique_together = [("name", "city")]


class Shop(TortoiseModel):
    """Shop entity model."""
    name = fields.CharField(max_length=255)
    city = fields.ForeignKeyField("models.City")
    street = fields.ForeignKeyField("models.Street")
    time_open = fields.TimeField()
    time_close = fields.TimeField()

    @classmethod
    def filter(cls, *args: Q, **kwargs: Any) -> QuerySet["Shop"]:
        return (    # type: ignore
            super()
            .filter(*args, **kwargs)
            .select_related("shop", "city")
        )

    def __str__(self) -> str:
        return self.name

    class Meta:
        unique_together = [("name", "city", "street")]
