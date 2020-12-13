from api import get_estimated_txfee
from api.responsemodels import EstimatedTxFeeResponseModel
from exceptions import InsufficientFundsForTransactionException, NodeResponseException
import unittest
import unittest.mock as mock


class GetEstimatedTxFeeTests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_estimated_txfee_is_successful(self):
        payload = mock.MagicMock()
        payload.get_estimate_txfee_payload.return_value = {'dummy': 'values'}
        response = mock.MagicMock(status_code=200)
        response.json.return_value = 10000
        with mock.patch('requests.post', return_value=response):
            response = get_estimated_txfee(payload=payload, crosschain=True)
            assert isinstance(response, EstimatedTxFeeResponseModel)
            assert response.fee == 10000

    def test_estimated_txfee_raises_insufficient_funds_exception(self):
        payload = mock.MagicMock()
        payload.get_estimate_txfee_payload.return_value = {'dummy': 'values'}
        response = mock.MagicMock(status_code=400)
        response.json.return_value = {'errors': [{'message': 'Not enough funds to cover the target at address'}]}
        with mock.patch('requests.post', return_value=response):
            with self.assertRaises(InsufficientFundsForTransactionException):
                get_estimated_txfee(payload=payload, crosschain=False)

    def test_estimated_txfee_raises_noderesponseexception(self):
        payload = mock.MagicMock()
        payload.get_estimate_txfee_payload.return_value = {'dummy': 'values'}
        response = mock.MagicMock(status_code=400)
        response.json.return_value = {'errors': [{'message': 'Some other message goes here.'}]}
        with mock.patch('requests.post', return_value=response):
            with self.assertRaises(NodeResponseException):
                get_estimated_txfee(payload=payload, crosschain=False)


if __name__ == '__main__':
    unittest.main()
