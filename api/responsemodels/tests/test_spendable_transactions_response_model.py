from api.responsemodels import SpendableTransactionsResponseModel
from random import choice
import string
import unittest
import unittest.mock as mock
from utilities import Address, Network, Money, Outpoint


class SpendableTransactionsResponseModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.transaction_hash = self._generate_transaction_hash()
        self.cirrus_address = self._generate_cirrus_address()

    def tearDown(self) -> None:
        pass

    def _generate_transaction_hash(self) -> str:
        letters = '0123456789abcdef'
        return ''.join(choice(letters) for _ in range(64))

    def _generate_cirrus_address(self) -> Address:
        letters = string.ascii_letters + '0123456789'
        return Address(address='C' + ''.join(choice(letters) for _ in range(33)), network=Network.CIRRUS)

    def test_spendable_transaction_valid_transaction_list_is_successful(self):
        response = mock.MagicMock()
        response.json.return_value = {'transactions': [{'address': self.cirrus_address, 'id': self.transaction_hash, 'index': 0, 'amount': 100}]}
        trx = SpendableTransactionsResponseModel(response=response, network=Network.CIRRUS)
        assert len(trx.spendable) == 1
        assert isinstance(trx.spendable[0], Outpoint)
        assert trx.spendable[0].address == self.cirrus_address
        assert isinstance(trx.spendable[0].amount, Money)
        assert trx.spendable[0].amount == 100
        assert str(trx.spendable[0].amount) == '0.00000100'
        assert all(key in ('transactionId', 'index') for key in trx.spendable[0].serialize().keys())

    def test_spendable_transactions_response_model_catches_errors(self):
        response = mock.MagicMock()
        response.json.return_value = {'errors': ['an error']}
        trx = SpendableTransactionsResponseModel(response=response, network=Network.CIRRUS)
        assert len(trx.errors) == 1


if __name__ == '__main__':
    unittest.main()
