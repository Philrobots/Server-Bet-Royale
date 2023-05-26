import unittest
from typing import Optional
from mockito import mock
from main.infra.schemas.field.StringDumpIntLoadField import StringDumpIntLoadField


class StringDumpIntLoadFieldTest(unittest.TestCase):

    def setUp(self) -> None:
        self.INVALID_STRING = "cogneur"
        self.VALID_STRING = "123"
        self.VALID_INT = 123
        self.string_dump_int_load_field = StringDumpIntLoadField()

    def test_whenDeserializeInvalidString_thenRaiseValueError(self):
        with self.assertRaises(ValueError):
            self.string_dump_int_load_field._deserialize(self.INVALID_STRING, mock(Optional), mock(Optional))

    def test_whenDeserializeValidString_thenReturnCorrectValue(self):
        actual_int = self.string_dump_int_load_field._deserialize(self.VALID_STRING, mock(Optional), mock(Optional))
        self.assertEqual(self.VALID_INT, actual_int)

    def test_whenSerialize_thenReturnCorrectValue(self):
        actual_string = self.string_dump_int_load_field._serialize(self.VALID_INT, mock(Optional), mock(Optional))
        self.assertEqual(self.VALID_STRING, actual_string)
