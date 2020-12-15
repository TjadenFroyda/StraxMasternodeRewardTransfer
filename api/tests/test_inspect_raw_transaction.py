import pytest
from pytest_mock import MockerFixture
from api import SwaggerAPI
from exceptions import NodeResponseException
from .generators import generate_transaction_hash, generate_hexstring


def test_inspect_transaction_is_successful(mocker: MockerFixture):
    transaction = mocker.Mock(hex=generate_hexstring())
    response = mocker.MagicMock(status_code=200)
    response.json.return_value = {
        "hex": generate_hexstring(), "txid": generate_transaction_hash(), "hash": generate_transaction_hash(), "version": 1, "size": 181,
        "vsize": 154, "weight": 613, "locktime": 0, "vin": [{}], "vout": [{}]
    }
    mocker.patch('requests.post', return_value=response)
    api = SwaggerAPI()

    api.inspect_transaction(transaction=transaction)


def test_inspect_transaction_raises_noderesponseexception(mocker: MockerFixture):
    transaction = mocker.Mock(hex=generate_hexstring())
    mocker.patch('requests.post', return_value=mocker.MagicMock(status_code=400))
    api = SwaggerAPI()

    with pytest.raises(NodeResponseException):
        api.inspect_transaction(transaction=transaction)
