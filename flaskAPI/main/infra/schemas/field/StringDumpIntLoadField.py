import typing

from marshmallow.fields import Field


class StringDumpIntLoadField(Field):

    def _deserialize(self, string: str, *args, **kwargs):
        return int(string)

    def _serialize(self, value: int, *args, **kwargs):
        return str(value)
