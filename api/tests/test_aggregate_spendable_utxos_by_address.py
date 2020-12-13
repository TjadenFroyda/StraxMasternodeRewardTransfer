from api import aggregate_spendable_utxos_by_address
from exceptions import NodeResponseException
from random import choice
import string
import unittest
import unittest.mock as mock
from utilities import Address, Outpoint, Network


class AggregateSpendableUTXOByAddressTests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def _generate_transaction_hash(self) -> str:
        letters = '0123456789abcdef'
        return ''.join(choice(letters) for _ in range(64))

    def _generate_cirrus_address(self) -> Address:
        letters = string.ascii_letters + '0123456789'
        return Address(address='C' + ''.join(choice(letters) for _ in range(33)), network=Network.CIRRUS)

    def test_aggregate_spendable_utxos_by_address_is_successful(self):
        response = mock.MagicMock(status_code=200)
        sending_address = self._generate_cirrus_address()
        num_transactions = 7
        response.json.return_value = {'transactions': [
            {'address': sending_address, 'id': self._generate_transaction_hash(), 'index': 0, 'amount': 100} for _ in range(num_transactions)
        ]}
        with mock.patch('requests.get', return_value=response):
            response = aggregate_spendable_utxos_by_address(wallet_name='test', min_conf=0, network=Network.CIRRUS)
            assert isinstance(response, dict)
            assert str(sending_address) in response.keys()
            assert len(response.get(str(sending_address))) == num_transactions
            assert isinstance(response.get(str(sending_address))[0], Outpoint)
            assert all(key in ('transactionId', 'index') for key in response.get(str(sending_address))[0].serialize().keys())

    def test_aggregate_spendable_utxos_by_address_raises_noderesponseexception(self):
        with mock.patch('requests.get', return_value=mock.MagicMock(status_code=400)):
            with self.assertRaises(NodeResponseException):
                aggregate_spendable_utxos_by_address(wallet_name='test', min_conf=0, network=Network.CIRRUS)


if __name__ == '__main__':
    unittest.main()
