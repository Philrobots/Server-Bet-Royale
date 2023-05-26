from bson import ObjectId
from bson.errors import InvalidId

from main.domain.exception.InvalidDomainIdException import InvalidDomainIdException


class DomainId:

    def __init__(self, identifier=None):
        if identifier is None:
            self.__identifier = self.__generate_object_id()
        else:
            self.__identifier = self.__validate_id(identifier)

    def to_object_id(self) -> ObjectId:
        return self.__identifier

    # todo replace usages for string dunder
    def to_string(self) -> str:
        return str(self.__identifier)

    def __generate_object_id(self):
        return ObjectId()

    def __validate_id(self, identifier: str):
        try:
            return ObjectId(identifier)
        except InvalidId:
            raise InvalidDomainIdException

    def __hash__(self):
        return hash(self.__identifier)

    def __eq__(self, other):
        if not isinstance(other, DomainId):
            return False
        return self.to_string() == other.to_string()

    def __str__(self):
        return str(self.__identifier)
