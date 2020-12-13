from api import send_transaction
from api.responsemodels import SendTransactionResponseModel
from exceptions import NodeResponseException
from random import choice
import unittest
import unittest.mock as mock


class SendTransactionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.hex_string = self._generate_hexstring()

    def tearDown(self) -> None:
        pass

    def _generate_hexstring(self) -> str:
        letters = '0123456789abcdef'
        return ''.join(choice(letters) for _ in range(128))

    def _generate_transaction_hash(self) -> str:
        letters = '0123456789abcdef'
        return ''.join(choice(letters) for _ in range(64))

    def test_send_transaction_is_successful(self):
        payload = mock.Mock(hex=self.hex_string)
        response = mock.MagicMock(status_code=200)
        response.json.return_value = {'transactionId': self._generate_transaction_hash(), 'outputs': ['output1', 'output2']}
        with mock.patch('requests.post', return_value=response):
            response = send_transaction(payload)
            assert isinstance(response, SendTransactionResponseModel)

    def test_send_transaction_raises_noderesponseexception(self):
        payload = mock.Mock(hex=self.hex_string)
        with mock.patch('requests.post', return_value=mock.MagicMock(status_code=400)):
            with self.assertRaises(NodeResponseException):
                send_transaction(payload)


if __name__ == '__main__':
    unittest.main()
