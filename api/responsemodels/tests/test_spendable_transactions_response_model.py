from pytest_mock import MockerFixture
from api.responsemodels import SpendableTransactionsResponseModel
from utilities import Network, Money, Outpoint
from .generators import generate_cirrus_address, generate_transaction_hash


def test_spendable_transaction_valid_transaction_list_is_successful(mocker: MockerFixture):
    response = mocker.MagicMock()
    response.json.return_value = {'transactions': [{'address': generate_cirrus_address(), 'id': generate_transaction_hash(), 'index': 0, 'amount': 100}]}

    trx = SpendableTransactionsResponseModel(response=response, network=Network.CIRRUS)

    assert len(trx.spendable) == 1
    assert isinstance(trx.spendable[0], Outpoint)
    assert trx.spendable[0].address == response.json()['transactions'][0]['address']
    assert isinstance(trx.spendable[0].amount, Money)
    assert trx.spendable[0].amount == 100
    assert str(trx.spendable[0].amount) == '0.00000100'
    assert all(key in ('transactionId', 'index') for key in trx.spendable[0].serialize().keys())

