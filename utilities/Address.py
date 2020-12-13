from typing import Union
from . import Network


class Address:
    """A utility class for Addresses"""
    def __init__(self, address: Union['Address', str], network: Network):
        if not isinstance(address, str) and not isinstance(address, Address):
            raise TypeError('Can only initialize address with str or Address.')

        self._network = network
        self._address = self._validate(address)

    def __get__(self, instance, owner) -> str:
        return self._address

    def __str__(self) -> str:
        return self._address

    def __eq__(self, other: Union['Address', str]) -> bool:
        if isinstance(other, Address):
            return self._address == other._address
        elif isinstance(other, str):
            return self._address == other
        else:
            raise TypeError('Can only compare with address or str.')

    def _validate(self, address: Union['Address', str]) -> str:
        # Convert the address back to string and re-validate both string and network.
        if isinstance(address, Address):
            address = str(address)

        # Validate string format.
        if len(address) != 34:
            # Segwit addresses not supported (length 42).
            raise ValueError('Address string length must be 34 char long.')
        if not address.isalnum():
            raise ValueError('Non-alphanumeric characters detected in address.')

        # Validate network.
        if self._network is Network.STRAX:
            if address[0] not in ['X', 'y']:
                # Segwit addresses not supported (start in strax1q).
                raise ValueError('Strax addresses must start with X or y')
            return address
        elif self._network is Network.CIRRUS:
            if address[0] not in ['C', 'c']:
                # Segwit addresses not supported (start in tb1q).
                raise ValueError('Cirrus addresses must start with C or c')
            return address
        else:
            raise ValueError('Invalid network.')
