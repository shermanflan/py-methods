

from marshmallow import EXCLUDE
from marshmallow.fields import Decimal
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from .model import GlobalMedList


# TODO: Consider using simplejson over marshmallow.
# Decimal not serialized to JSON
# https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Decimal
class GlobalMedListSchema(SQLAlchemySchema):
    # Ignore unknown fields
    class Meta:
        unknown = EXCLUDE
        ordered = True
        model = GlobalMedList
        load_instance = True

    Id = auto_field()
    Name = auto_field()
    Dose = Decimal(places=2, as_string=True)
    Created = auto_field()


MedSchema = GlobalMedListSchema()
