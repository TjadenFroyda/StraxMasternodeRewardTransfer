import unittest
import unittest.mock as mock
from random import choice
from utilities import Money
from api.responsemodels import BuildTransactionResponseModel


class BuildTransactionResponseModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_transaction = self._generate_transaction_hash()
        self.mock_hexstring = self._generate_hexstring()

    def tearDown(self) -> None:
        pass

    def _generate_transaction_hash(self) -> str:
        letters = '0123456789abcdef'
        return ''.join(choice(letters) for _ in range(64))

    def _generate_hexstring(self) -> str:
        letters = '0123456789abcdef'
        return ''.join(choice(letters) for _ in range(128))

    def test_build_transaction_response_model_fee_in_satoshis_is_successful(self):
        response = mock.MagicMock()

        response.json.return_value = {'transactionId': self.mock_transaction, 'hex': self.mock_hexstring, 'fee': 10000}
        trx = BuildTransactionResponseModel(response)
        assert trx.fee == 10000
        assert isinstance(trx.fee, Money)
        assert str(trx.fee) == '0.00010000'

    def test_build_transaction_response_model_float_fee_raises_valueerror(self):
        response = mock.MagicMock()
        response.json.return_value = {'transactionId': self.mock_transaction, 'hex': self.mock_hexstring, 'fee': 0.00010000}
        with self.assertRaises(ValueError):
            BuildTransactionResponseModel(response)

        with self.assertRaises(ValueError):
            response.json.return_value = {'transactionId': self.mock_transaction, 'hex': self.mock_hexstring, 'fee': 10000.0}
            BuildTransactionResponseModel(response)

    def test_build_transaction_response_model_catches_errors(self):
        response = mock.MagicMock()
        response.json.return_value = {'errors': ['an error']}
        trx = BuildTransactionResponseModel(response)
        assert len(trx.errors) == 1


if __name__ == '__main__':
    unittest.main()
