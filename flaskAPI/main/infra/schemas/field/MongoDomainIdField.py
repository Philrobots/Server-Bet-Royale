from bson import ObjectId
from marshmallow import ValidationError
from marshmallow.fields import Field

from main.domain.exception.InvalidDomainIdException import InvalidDomainIdException
from main.domain.identifiers.DomainId import DomainId


class MongoDomainIdField(Field):

    def _serialize(self, domain_id: DomainId, *args, **kwargs):
        return domain_id.to_object_id()

    def _deserialize(self, value: str, *args, **kwargs):
        try:
            if not isinstance(value, ObjectId):
                raise ValidationError("")
            return DomainId(str(value))
        except InvalidDomainIdException:
            raise ValidationError("Invalid Id format: " + value)
        except ValidationError:
            raise ValidationError("Invalid Type for Id: " + str(value) + ", must be in string format")
