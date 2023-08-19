import unittest
from main.domain.exception.InvalidDomainIdException import InvalidDomainIdException
from main.domain.identifiers.DomainId import DomainId
from main.domain.gift.GiftFactory import GiftFactory


class GiftFactoryTest(unittest.TestCase):
    
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.gift_factory = GiftFactory()

    def test_whenToString_thenReturnValidString(self):
        uuid = "5fb6d855d90e6886f6614424"
        gift = self.gift_factory.create(DomainId(uuid))
        
        self.assertEqual(gift.price, 50)
