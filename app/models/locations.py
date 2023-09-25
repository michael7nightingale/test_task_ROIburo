from tortoise import fields, BaseDBAsyncClient
from tortoise.expressions import Q

from typing import Optional, Any

from .base import TortoiseModel


class City(TortoiseModel):
    """City entity model."""
    name = fields.CharField(unique=True, index=True, max_length=255)

    def __str__(self) -> str:
        return f"г. {self.name}"

    @classmethod
    async def get_or_none(
        cls, *args: Q, using_db: Optional[BaseDBAsyncClient] = None, **kwargs: Any
    ) -> Optional["City"]:
        """`get_or_none` method optimization."""
        return await (
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
