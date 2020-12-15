from decimal import Decimal
import requests as req
from typing import Union
from utilities import Money
SATOSHI_CONVERSION = Decimal(1e8)


class BuildTransactionResponseModel:
    """Response model for build-transaction api endpoint."""
    def __init__(self, response: req.Response):
        response = response.json()
        self._data = {}
        self.transaction_id = response.get('transactionId', None)
        self.hex = response.get('hex', None)
        self.fee = response.get('fee', None)

    @property
    def transaction_id(self) -> str:
        return self._data.get('transactionId', None)

    @transaction_id.setter
    def transaction_id(self, val: str) -> None:
        if not isinstance(val, str):
            raise ValueError('transaction_id must be a str.')
        if len(val) != 64:
            raise ValueError('transaction_id must be 64 char long.')
        self._data['transactionId'] = val

    @property
    def hex(self) -> str:
        return self._data.get('hex', None)

    @hex.setter
    def hex(self, val: str) -> None:
        if not isinstance(val, str):
            raise ValueError('hex must be a str.')
        self._data['hex'] = val

    @property
    def fee(self) -> Money:
        return self._data.get('fee', None)

    @fee.setter
    def fee(self, val: Union[int, Money]) -> None:
        if not isinstance(val, int) and not isinstance(val, Money):
            raise ValueError('fee must be int or Money.')
        self._data['fee'] = Money(val)
