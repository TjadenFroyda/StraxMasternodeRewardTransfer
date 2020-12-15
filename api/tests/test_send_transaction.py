import pytest
from pytest_mock import MockerFixture
from api import SwaggerAPI
from exceptions import NodeResponseException
from .generators import generate_hexstring, generate_transaction_hash


def test_send_transaction_is_successful(mocker: MockerFixture):
    transaction = mocker.Mock(hex=generate_hexstring())
    response = mocker.MagicMock(status_code=200)
    response.json.return_value = {'transactionId': generate_transaction_hash(), 'outputs': ['output1', 'output2']}
    mocker.patch('requests.post', return_value=response)
    api = SwaggerAPI()

    api.send_transaction(transaction=transaction)


def test_send_transaction_raises_noderesponseexception(mocker: MockerFixture):
    transaction = mocker.Mock(hex=generate_hexstring())
    mocker.patch('requests.post', return_value=mocker.MagicMock(status_code=400))
    api = SwaggerAPI()

    with pytest.raises(NodeResponseException):
        api.send_transaction(transaction=transaction)
