from random import choice
import string
import unittest
from utilities import Address, Network, Money, Outpoint


class OutputTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cirrus_address = self._generate_cirrus_address()
        self.strax_address = self._generate_strax_address()
        self.transaction_hash = self._generate_transaction_hash()

    def tearDown(self) -> None:
        pass

    def _generate_cirrus_address(self) -> Address:
        letters = string.ascii_letters + '0123456789'
        return Address(address='C' + ''.join(choice(letters) for _ in range(33)), network=Network.CIRRUS)

    def _generate_strax_address(self) -> Address:
        letters = string.ascii_letters + '0123456789'
        return Address(address='X' + ''.join(choice(letters) for _ in range(33)), network=Network.STRAX)

    def _generate_transaction_hash(self) -> str:
        letters = '0123456789abcdef'
        return ''.join(choice(letters) for _ in range(64))

    def test_outpoint_is_successful(self):
        outpoint = Outpoint(network=Network.CIRRUS, item={'address': self.cirrus_address, 'id': self.transaction_hash, 'index': 0, 'amount': Money(100)})
        assert outpoint.address == self.cirrus_address
        assert all(key in ('transactionId', 'index') for key in outpoint.serialize().keys())
        assert str(outpoint) == str({'transactionId': self.transaction_hash, 'index': 0})
        assert str(outpoint.serialize()) == str({'transactionId': self.transaction_hash, 'index': 0})

    def test_output_network_mismatch(self):
        with self.assertRaises(ValueError):
            Outpoint(network=Network.STRAX, item={'address': self.cirrus_address, 'id': self.transaction_hash, 'index': 0, 'amount': Money(100)})
        with self.assertRaises(ValueError):
            Outpoint(network=Network.CIRRUS, item={'address': self.strax_address, 'id': self.transaction_hash, 'index': 0, 'amount': Money(100)})

    def test_outpoint_serialization_exception_missing_values(self):
        with self.assertRaises(TypeError):
            outpoint = Outpoint(network=Network.CIRRUS, item={'address': self.cirrus_address, 'index': 0, 'amount': Money(100)})
            outpoint.serialize()


if __name__ == '__main__':
    unittest.main()
