from api import inspect_raw_transaction
from api.responsemodels import InspectRawTransactionResponseModel
from exceptions import NodeResponseException
from random import choice
import unittest
import unittest.mock as mock


class InspectRawTransactionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.hex_string = self._generate_hexstring()

    def tearDown(self) -> None:
        pass

    def _generate_transaction_hash(self) -> str:
        letters = '0123456789abcdef'
        return ''.join(choice(letters) for _ in range(64))

    def _generate_hexstring(self) -> str:
        letters = '0123456789abcdef'
        return ''.join(choice(letters) for _ in range(128))

    def test_inspect_raw_transaction_is_successful(self):
        payload = mock.Mock(hex=self.hex_string)
        response = mock.MagicMock(status_code=200)
        response.json.return_value = {
            "hex": self._generate_hexstring(), "txid": self._generate_transaction_hash(), "hash": self._generate_transaction_hash(), "version": 1, "size": 181,
            "vsize": 154, "weight": 613, "locktime": 0, "vin": [{}], "vout": [{}]
        }
        with mock.patch('requests.post', return_value=response):
            response = inspect_raw_transaction(payload)
            assert isinstance(response, InspectRawTransactionResponseModel)

    def test_inspect_raw_transaction_raises_noderesponseexception(self):
        payload = mock.Mock(hex=self.hex_string)
        with mock.patch('requests.post', return_value=mock.MagicMock(status_code=400)):
            with self.assertRaises(NodeResponseException):
                inspect_raw_transaction(payload)


if __name__ == '__main__':
    unittest.main()
