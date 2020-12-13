from api.responsemodels import EstimatedTxFeeResponseModel
import unittest
import unittest.mock as mock
from utilities import Money


class EstimatedTxFeeResponseModelTests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_estimated_txfee_response_model_large_fee_raises_valueerror(self):
        response = mock.MagicMock()
        response.json.return_value = 500000000
        with self.assertRaises(ValueError):
            EstimatedTxFeeResponseModel(response)

    def test_estimated_txfee_response_model_reasonable_fee_is_successful(self):
        response = mock.MagicMock()
        response.json.return_value = 10000
        trx = EstimatedTxFeeResponseModel(response)
        assert trx.fee == 10000
        assert isinstance(trx.fee, Money)
        assert str(trx.fee) == '0.00010000'

    def test_build_transaction_response_model_catches_errors(self):
        response = mock.MagicMock()
        response.json.return_value = {'errors': ['an error']}
        trx = EstimatedTxFeeResponseModel(response)
        assert len(trx.errors) == 1


if __name__ == '__main__':
    unittest.main()
