from requests import Response


class InspectTransactionResponseModel:
    """Response Model for decoderawtransaction api endpoint."""
    def __init__(self, response: Response):
        response = response.json()
        self._data = {}
        self.transaction_id = response.get('txid', None)
        self.hex = response.get('hex', None)
        self.hash = response.get('hash', None)
        self.version = response.get('version', None)
        self.size = response.get('size', None)
        self.vsize = response.get('vsize', None)
        self.weight = response.get('weight', None)
        self.locktime = response.get('locktime', None)
        self.vin = response.get('vin', None)
        self.vout = response.get('vout', None)

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
            raise ValueError('hex must be a str')
        self._data['hex'] = val

    @property
    def hash(self) -> str:
        return self._data.get('hash', None)

    @hash.setter
    def hash(self, val: str) -> None:
        if not isinstance(val, str):
            raise ValueError('hash must be a str')
        self._data['hash'] = val

    @property
    def version(self) -> int:
        return self._data.get('version', None)

    @version.setter
    def version(self, val: int) -> None:
        if not isinstance(val, int):
            raise ValueError('version must be an int')
        self._data['version'] = val

    @property
    def size(self) -> int:
        return self._data.get('size', None)

    @size.setter
    def size(self, val: int) -> None:
        if not isinstance(val, int):
            raise ValueError('size must be an int')
        self._data['size'] = val

    @property
    def vsize(self) -> int:
        return self._data.get('vsize', None)

    @vsize.setter
    def vsize(self, val: int) -> None:
        if not isinstance(val, int):
            raise ValueError('size must be an int')
        self._data['vsize'] = val

    @property
    def locktime(self) -> int:
        return self._data.get('locktime', None)

    @locktime.setter
    def locktime(self, val: int) -> None:
        if not isinstance(val, int):
            raise ValueError('locktime must be an int')
        self._data['locktime'] = val

    @property
    def vin(self) -> list:
        return self._data.get('vin', None)

    @vin.setter
    def vin(self, val: list) -> None:
        if not isinstance(val, list):
            raise ValueError('vin must be a list')
        self._data['vin'] = val

    @property
    def vout(self) -> list:
        return self._data.get('vout', None)

    @vout.setter
    def vout(self, val: list) -> None:
        if not isinstance(val, list):
            raise ValueError('vout must be a list')
        self._data['vout'] = val

    def serialize(self):
        return {k: str(v) for k, v in self._data.items()}

    def __str__(self):
        return str(self.serialize())
