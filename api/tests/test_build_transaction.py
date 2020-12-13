from api import build_transaction
from api.responsemodels import BuildTransactionResponseModel
from exceptions import NodeResponseException, RecommendedFeeTooHighException, FeeTooLowException
from random import choice
import unittest
import unittest.mock as mock


class BuildTransactionTests(unittest.TestCase):
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

    def test_build_transaction_is_successful(self):
        payload = mock.MagicMock()
        payload.get_build_transaction_payload.return_value = {'dummy': 'values'}
        response = mock.MagicMock(status_code=200)
        response.json.return_value = {'transactionId': self._generate_transaction_hash(), 'hex': self._generate_hexstring(), 'fee': 10000}
        with mock.patch('requests.post', return_value=response):
            response = build_transaction(payload=payload, crosschain=True)
            assert isinstance(response, BuildTransactionResponseModel)

    def test_build_transaction_raises_noderesponseexception_for_invalid_password(self):
        payload = mock.MagicMock()
        payload.get_build_transaction_payload.return_value = {'dummy': 'values'}
        response = mock.MagicMock(status_code=400)
        response.json.return_value = {'errors': [{'message': 'Invalid password (or invalid Network)'}]}
        with mock.patch('requests.post', return_value=response):
            with self.assertRaises(NodeResponseException):
                build_transaction(payload=payload, crosschain=False)

    def test_build_transaction_raises_noderesponseexception_general_error(self):
        payload = mock.MagicMock()
        payload.get_build_transaction_payload.return_value = {'dummy': 'values'}
        response = mock.MagicMock(status_code=400)
        response.json.return_value = {'errors': [{'message': 'General error'}]}
        with mock.patch('requests.post', return_value=response):
            with self.assertRaises(NodeResponseException) as ctx:
                build_transaction(payload=payload, crosschain=False)
                assert ctx.exception.message == 'Error building crosschain transaction.'

    def test_build_transaction_raises_recommended_fee_too_high_exception(self):
        payload = mock.MagicMock()
        payload.get_build_transaction_payload.return_value = {'dummy': 'values'}
        response = mock.MagicMock(status_code=400)
        response.json.return_value = {'errors': [{'message': 'The policy minimum is 5.0.'}]}
        with mock.patch('requests.post', return_value=response):
            with self.assertRaises(RecommendedFeeTooHighException) as ctx:
                build_transaction(payload=payload, crosschain=False)
            assert ctx.exception.fee == int(5.0 * 1e8)

    def test_build_transaction_raises_fee_too_low_exception(self):
        payload = mock.MagicMock()
        payload.get_build_transaction_payload.return_value = {'dummy': 'values'}
        response = mock.MagicMock(status_code=400)
        response.json.return_value = {'errors': [{'message': 'The policy minimum is 0.00012345.'}]}
        with mock.patch('requests.post', return_value=response):
            with self.assertRaises(FeeTooLowException) as ctx:
                build_transaction(payload=payload, crosschain=False)
            assert ctx.exception.recommended_fee == 12345


if __name__ == '__main__':
    unittest.main()
