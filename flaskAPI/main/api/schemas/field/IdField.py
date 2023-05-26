from marshmallow.fields import Field
from main.domain.identifiers.DomainId import DomainId


class IdField(Field):

    def _serialize(self, domain_id: DomainId, *args, **kwargs):
        return domain_id.to_string()

    def _deserialize(self, value: str, *args, **kwargs):
        return DomainId(value)
