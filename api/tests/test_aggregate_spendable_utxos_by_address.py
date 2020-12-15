import pytest
from pytest_mock import MockerFixture
from api import SwaggerAPI
from exceptions import NodeResponseException
from utilities import Outpoint, Network
from .generators import generate_cirrus_address, generate_transaction_hash


def test_aggregate_spendable_utxos_by_address_is_successful(mocker: MockerFixture):
    response = mocker.MagicMock(status_code=200)
    sending_address = generate_cirrus_address()
    num_transactions = 7
    response.json.return_value = {'transactions': [
        {'address': sending_address, 'id': generate_transaction_hash(), 'index': 0, 'amount': 100} for _ in range(num_transactions)
    ]}
    mocker.patch('requests.get', return_value=response)
    api = SwaggerAPI()

    response = api.get_spendable_transactions(wallet_name='test', min_conf=0, network=Network.CIRRUS)

    assert isinstance(response, dict)
    assert str(sending_address) in response.keys()
    assert len(response.get(str(sending_address))) == num_transactions
    assert isinstance(response.get(str(sending_address))[0], Outpoint)
    assert all(key in ('transactionId', 'index') for key in response.get(str(sending_address))[0].serialize().keys())


def test_aggregate_spendable_utxos_by_address_raises_noderesponseexception(mocker: MockerFixture):
    mocker.patch('requests.get', return_value=mocker.MagicMock(status_code=400))
    api = SwaggerAPI()

    with pytest.raises(NodeResponseException):
        api.get_spendable_transactions(wallet_name='test', min_conf=0, network=Network.CIRRUS)
