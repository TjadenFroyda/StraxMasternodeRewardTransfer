from typing import Union
from . import Network, Address, Money


class Recipient:
    def __init__(self, item: dict, network: Network):
        self._data = {}
        self._network = network
        self.destination_address = Address(address=item.get('destinationAddress', None), network=network)

    @property
    def destination_address(self) -> Address:
        return self._data.get('destinationAddress', None)

    @destination_address.setter
    def destination_address(self, val: Address) -> None:
        if not isinstance(val, Address):
            raise TypeError('destination_address must be a Address.')
        self._data['destinationAddress'] = Address(address=val, network=self._network)

    @property
    def amount(self) -> Money:
        return self._data.get('amount', None)

    @amount.setter
    def amount(self, val: Union[Money, int]) -> None:
        if not isinstance(val, Money) and not isinstance(val, int):
            raise TypeError('amount must be Money or int.')
        self._data['amount'] = Money(val)

    def serialize(self) -> dict:
        """Serializes a recipient for transaction building."""
        if self.amount is None:
            raise ValueError('amount not set.')
        return {k: str(v) for k, v in self._data.items()}

    def __str__(self) -> str:
        return str(self.serialize())
