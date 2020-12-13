from api.responsemodels import InspectRawTransactionResponseModel
from random import choice
import unittest
import unittest.mock as mock


class InspectRawTransactionResponseModelTests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def _generate_transaction_hash(self) -> str:
        letters = '0123456789abcdef'
        return ''.join(choice(letters) for _ in range(64))

    def _generate_hexstring(self) -> str:
        letters = '0123456789abcdef'
        return ''.join(choice(letters) for _ in range(128))

    def test_inspect_raw_transaction_response_model_catches_errors(self):
        response = mock.MagicMock()
        response.json.return_value = {'errors': ['an error']}
        trx = InspectRawTransactionResponseModel(response)
        assert len(trx.errors) == 1

    def test_inspect_raw_transaction_response_model(self):
        mock_raw_transaction = {
            'txid': self._generate_transaction_hash(),
            'hex': self._generate_hexstring(),
            'hash': self._generate_transaction_hash(),
            'version': 0,
            'size': 1,
            'vsize': 1,
            'weight': 1,
            'locktime': 1,
            'vin': [],
            'vout': []
        }
        response = mock.MagicMock()
        response.json.return_value = mock_raw_transaction
        trx = InspectRawTransactionResponseModel(response)
        assert trx.transaction_id == mock_raw_transaction['txid']
        assert trx.hex == mock_raw_transaction['hex']


if __name__ == '__main__':
    unittest.main()
