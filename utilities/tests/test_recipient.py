from random import choice
import string
import unittest
from utilities import Address, Network, Money, Recipient


class RecipientTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cirrus_address = self._generate_cirrus_address()

    def tearDown(self) -> None:
        pass

    def _generate_cirrus_address(self) -> Address:
        letters = string.ascii_letters + '0123456789'
        return Address(address='C' + ''.join(choice(letters) for _ in range(33)), network=Network.CIRRUS)

    def test_recipient_is_successful(self):
        recipient = Recipient(network=Network.CIRRUS, item={'destinationAddress': self.cirrus_address})
        recipient.amount = 10000
        assert recipient.destination_address == self.cirrus_address
        assert isinstance(recipient.amount, Money)
        assert recipient.amount == 10000
        assert str(recipient.amount) == '0.00010000'
        assert str(recipient) == str({'destinationAddress': str(self.cirrus_address), 'amount': str(recipient.amount)})
        assert str(recipient.serialize()) == str({'destinationAddress': str(self.cirrus_address), 'amount': str(recipient.amount)})

    def test_recipient_decimal_amount_raises_valueerror(self):
        recipient = Recipient(network=Network.CIRRUS, item={'destinationAddress': self.cirrus_address})
        with self.assertRaises(TypeError):
            recipient.amount = 0.00001


if __name__ == '__main__':
    unittest.main()
