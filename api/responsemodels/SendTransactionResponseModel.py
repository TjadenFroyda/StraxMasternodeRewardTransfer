from requests import Response


class SendTransactionResponseModel:
    """Response model for send-transaction api endpoint."""
    def __init__(self, response: Response):
        response = response.json()
        self._data = {}
        if isinstance(response, dict) and 'errors' in response.keys():
            self.errors = response.get('errors', [])
        else:
            self.transactionId = response.get('transactionId', None)
            self.outputs = response.get('outputs', None)

    @property
    def transaction_id(self) -> str:
        return self._data.get('transactionId', None)

    @transaction_id.setter
    def transaction_id(self, val: str) -> None:
        if not isinstance(val, str):
            raise ValueError('transaction_id must be a str.')
        self._data['transactionId'] = val

    @property
    def outputs(self) -> list:
        return self._data.get('outputs', [])

    @outputs.setter
    def outputs(self, val: list):
        if not isinstance(val, list):
            raise ValueError('outputs must be a list.')
        self._data['outputs'] = val

    @property
    def errors(self) -> list:
        return self._data.get('errors', [])

    @errors.setter
    def errors(self, val: list):
        if not isinstance(val, list):
            raise ValueError('errors must be a list.')
        self._data['errors'] = val

    def __str__(self):
        return str(self._data)