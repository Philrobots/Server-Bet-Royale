import unittest
from bson import ObjectId

from main.domain.exception.InvalidDomainIdException import InvalidDomainIdException
from main.domain.identifiers.DomainId import DomainId


class DomainIdTest(unittest.TestCase):

    def test_whenToString_thenReturnValidString(self):
        uuid = "5fb6d855d90e6886f6614424"
        domain_id = DomainId(uuid)
        self.assertEqual(uuid, domain_id.to_string())

    def test_whenToUuid_thenReturnValidUuid(self):
        uuid = "5fb6d855d90e6886f6614424"
        object_id = ObjectId(uuid)
        domain_id = DomainId(uuid)
        self.assertEqual(object_id, domain_id.to_object_id())

    def test_givenIdenticalDomainId_whenEqual_thenIsTrue(self):
        uuid = "5fb6d855d90e6886f6614424"
        domain_id_1 = DomainId(uuid)
        domain_id_2 = DomainId(uuid)
        self.assertTrue(domain_id_1 == domain_id_2)

    def test_givenDifferentDomainId_whenEqual_thenIsFalse(self):
        uuid = "5fb6d855d90e6886f6614424"
        uuid2 = "5fb6d855d90e6886f6614425"
        domain_id_1 = DomainId(uuid)
        domain_id_2 = DomainId(uuid2)
        self.assertFalse(domain_id_1 == domain_id_2)

    def test_givenDifferentObjectType_whenEqual_thenIsFalse(self):
        uuid = "5fb6d855d90e6886f6614424"
        object_id = ObjectId(uuid)
        domain_id = DomainId(uuid)
        self.assertFalse(object_id == domain_id)

    def test_withInvalidId_thenReturnInvalidDomainIdException(self):
        with self.assertRaises(InvalidDomainIdException):
            DomainId("ppipipcaca")

    def test_whenRemoveFromArray_thenProperlyRemoves(self):
        x = []
        id = DomainId()
        x.append(id)
        x.remove(id)
        self.assertEqual(0, len(x))
