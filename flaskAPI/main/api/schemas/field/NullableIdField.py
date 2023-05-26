
from marshmallow import ValidationError
from marshmallow.fields import Field
from main.domain.exception.InvalidDomainIdException import InvalidDomainIdException
from main.domain.identifiers.DomainId import DomainId


class NullableIdField(Field):

    def _serialize(self, domain_id: DomainId | None, *args, **kwargs):
        return str(domain_id) if domain_id is not None else None

    def _deserialize(self, value: str| None, *args, **kwargs):
        try:
            if value is None:
                return None
            if not isinstance(value, str):
                raise ValidationError("Invalid Type for Id: " + str(value) + ", must be in string format")
            return DomainId(str(value))
        except InvalidDomainIdException:
            raise ValidationError("Invalid Id format: " + value)
        except ValidationError:
            raise ValidationError("Invalid Type for Id: " + str(value) + ", must be in string format")