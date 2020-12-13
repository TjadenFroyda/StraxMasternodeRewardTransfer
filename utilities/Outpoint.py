from typing import Union
from . import Network, Address, Money


class Outpoint:
    def __init__(self, item: dict, network: Network):
        self._network = network
        self._data = {}
        self.address = Address(address=item.get('address', None), network=network)
        self.transaction_id = item.get('id', None)
        self.index = int(item.get('index', 0))
        self.amount = Money(item.get('amount', None))

    @property
    def address(self) -> Address:
        return self._data.get('address', None)

    @address.setter
    def address(self, val: Address) -> None:
        if not isinstance(val, Address):
            raise TypeError('address must be an Address.')
        self._data['address'] = Address(address=val, network=self._network)

    @property
    def transaction_id(self) -> str:
        return self._data.get('transactionId', None)

    @transaction_id.setter
    def transaction_id(self, val: str) -> None:
        if not isinstance(val, str):
            raise TypeError('transaction_id must be a str.')
        self._data['transactionId'] = val

    @property
    def index(self) -> str:
        return self._data.get('index', None)

    @index.setter
    def index(self, val: int) -> None:
        if not isinstance(val, int):
            raise TypeError('index must be an int.')
        self._data['index'] = val

    @property
    def amount(self) -> Money:
        return self._data.get('amount', None)

    @amount.setter
    def amount(self, val: Union[Money, int]) -> None:
        if not isinstance(val, Money) and not isinstance(val, int):
            raise TypeError('amount must be Money or int.')
        self._data['amount'] = Money(val)

    def serialize(self) -> dict:
        """Serializes an outpoint into a dictionary with transactionId and index keys for transaction building."""
        if self.transaction_id is None or self.index is None:
            raise ValueError('Both transaction_id and index must be set.')
        return {k: v for k, v in self._data.items() if k in ['transactionId', 'index']}

    def __str__(self) -> str:
        return str(self.serialize())
