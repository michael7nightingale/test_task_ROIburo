from tortoise import fields
from tortoise.models import Model

from uuid import uuid4


class TortoiseModel(Model):
    """Abstract orm model. Add UUID VARCHAR pk `id`."""
    id = fields.CharField(max_length=255, pk=True, default=lambda: str(uuid4()))

    def as_dict(self) -> dict:
        """Deserializes model instance to dictionary."""
        schema = self.describe()
        dicted = {field['name']: getattr(self, field['name']) for field in schema['data_fields']}
        dicted[schema['pk_field']['name']] = str(getattr(self, schema['pk_field']['name']))
        return dicted

    def update_from_dict(self, data: dict):
        """Override method for updating not null values."""
        return super().update_from_dict({k: v for k, v in data.items() if v is not None})

    class Meta:
        abstract = True     # entity is not creating, it is abstract
