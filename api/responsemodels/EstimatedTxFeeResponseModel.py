from requests import Response
from utilities import Money


class EstimatedTxFeeResponseModel:
    """Response model for estimate-txfee api endpoint."""
    def __init__(self, response: Response):
        response = response.json()
        self._data = {}
        if isinstance(response, dict):
            self.errors = response.get('errors', [])
        else:
            self.fee = int(response)

    @property
    def fee(self) -> Money:
        return self._data.get('fee', None)

    @fee.setter
    def fee(self, val: int) -> None:
        if not isinstance(val, int):
            raise ValueError('fee must be an int.')
        if val > 100000000:
            raise ValueError('fee is greater than 100000000')
        self._data['fee'] = Money(val)

    @property
    def errors(self) -> list:
        return self._data.get('errors', [])

    @errors.setter
    def errors(self, val: list):
        if not isinstance(val, list):
            raise ValueError('errors must be a list.')
        self._data['errors'] = val
