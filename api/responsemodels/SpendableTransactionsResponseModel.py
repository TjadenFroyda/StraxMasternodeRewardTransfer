from requests import Response
from utilities import Network, Outpoint


class SpendableTransactionsResponseModel:
    """Response model for spendable-transactions api endpoint."""
    def __init__(self, response: Response, network: Network):
        response = response.json()
        self._network = network
        self._data = {}
        self.spendable = response.get('transactions', [])

    @property
    def spendable(self) -> list:
        return self._data.get('spendable', None)

    @spendable.setter
    def spendable(self, val: list) -> None:
        if not isinstance(val, list):
            raise ValueError('Could not parse spendable transaction list.')
        self._data['spendable'] = [Outpoint(network=self._network, item=utxo) for utxo in val]
