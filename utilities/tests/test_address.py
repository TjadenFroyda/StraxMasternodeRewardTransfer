from random import choice
import string
import unittest
from utilities import Network, Address


class AddressTests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def _random_string_generator(self, length: int):
        letters = string.ascii_letters + '0123456789'
        return ''.join(choice(letters) for _ in range(length))

    def test_create_valid_address(self):
        strax_addr = 'X' + self._random_string_generator(33)
        assert Address(address=strax_addr, network=Network.STRAX) == strax_addr

        strax_federation_addr = 'y' + self._random_string_generator(33)
        assert Address(address=strax_federation_addr, network=Network.STRAX) == strax_federation_addr

        cirrus_addr = 'C' + self._random_string_generator(33)
        assert Address(address=cirrus_addr, network=Network.CIRRUS) == cirrus_addr

        cirrus_federation_addr = 'c' + self._random_string_generator(33)
        assert Address(address=cirrus_federation_addr, network=Network.CIRRUS) == cirrus_federation_addr

    def test_create_invalid_first_character(self):
        strax_addr = 'x' + self._random_string_generator(33)
        with self.assertRaises(ValueError):
            Address(address=strax_addr, network=Network.STRAX)

        strax_federation_addr = 'Y' + self._random_string_generator(33)
        with self.assertRaises(ValueError):
            Address(address=strax_federation_addr, network=Network.STRAX)

        cirrus_addr = 'd' + self._random_string_generator(33)
        with self.assertRaises(ValueError):
            Address(address=cirrus_addr, network=Network.CIRRUS)

    def test_create_address_too_long(self):
        strax_addr = 'X' + self._random_string_generator(36)
        with self.assertRaises(ValueError):
            Address(address=strax_addr, network=Network.STRAX)

        strax_federation_addr = 'y' + self._random_string_generator(36)
        with self.assertRaises(ValueError):
            Address(address=strax_federation_addr, network=Network.STRAX)

        cirrus_addr = 'C' + self._random_string_generator(36)
        with self.assertRaises(ValueError):
            Address(address=cirrus_addr, network=Network.CIRRUS)

        cirrus_federation_addr = 'c' + self._random_string_generator(36)
        with self.assertRaises(ValueError):
            Address(address=cirrus_federation_addr, network=Network.CIRRUS)

    def test_create_address_too_short(self):
        strax_addr = 'X' + self._random_string_generator(30)
        with self.assertRaises(ValueError):
            Address(address=strax_addr, network=Network.STRAX)

        strax_federation_addr = 'y' + self._random_string_generator(30)
        with self.assertRaises(ValueError):
            Address(address=strax_federation_addr, network=Network.STRAX)

        cirrus_addr = 'C' + self._random_string_generator(30)
        with self.assertRaises(ValueError):
            Address(address=cirrus_addr, network=Network.CIRRUS)

        cirrus_federation_addr = 'c' + self._random_string_generator(30)
        with self.assertRaises(ValueError):
            Address(address=cirrus_federation_addr, network=Network.CIRRUS)

    def test_create_address_invalid_characters(self):
        strax_addr = 'X' + self._random_string_generator(33)
        strax_addr = strax_addr[:16] + '[' + strax_addr[17:]
        with self.assertRaises(ValueError):
            Address(address=strax_addr, network=Network.STRAX)

        strax_federation_addr = 'y' + self._random_string_generator(33)
        strax_federation_addr = strax_federation_addr[:16] + '[' + strax_federation_addr[17:]
        with self.assertRaises(ValueError):
            Address(address=strax_federation_addr, network=Network.STRAX)

        cirrus_addr = 'C' + self._random_string_generator(33)
        cirrus_addr = cirrus_addr[:16] + '[' + cirrus_addr[17:]
        with self.assertRaises(ValueError):
            Address(address=cirrus_addr, network=Network.CIRRUS)

        cirrus_federation_addr = 'c' + self._random_string_generator(33)
        cirrus_federation_addr = cirrus_federation_addr[:16] + '[' + cirrus_federation_addr[17:]
        with self.assertRaises(ValueError):
            Address(address=cirrus_federation_addr, network=Network.CIRRUS)
