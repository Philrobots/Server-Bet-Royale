from bson import ObjectId
from marshmallow import ValidationError
from marshmallow.fields import Field

from main.domain.exception.InvalidDomainIdException import InvalidDomainIdException
from main.domain.identifiers.DomainId import DomainId

class NullableMongoDomainIdField(Field):

    def _serialize(self, domain_id: DomainId | None, *args, **kwargs):
        return domain_id.to_object_id() if domain_id is not None else None

    def _deserialize(self, value: ObjectId | None, *args, **kwargs):
        try:
            if value is None:
                return None
            if not isinstance(value, ObjectId):
                raise ValidationError("")
            return DomainId(str(value))
        except InvalidDomainIdException:
            raise ValidationError("Invalid Id format: " + value)
        except ValidationError:
            raise ValidationError("Invalid Type for Id: " + str(value) + ", must be in string format")