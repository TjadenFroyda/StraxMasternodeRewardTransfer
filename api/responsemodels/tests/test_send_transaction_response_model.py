from pytest_mock import MockerFixture
from api.responsemodels import SendTransactionResponseModel
from .generators import generate_transaction_hash, generate_cirrus_address, generate_strax_address


def test_send_transaction_response_model_consolidation_transaction(mocker: MockerFixture):
    amount = 100000000
    mock_response = {
        'transactionId': generate_transaction_hash(),
        'outputs': [{'address': str(generate_cirrus_address()), 'amount': amount}, {'amount': 0, 'opReturnData': str(generate_strax_address())}]
    }

    response = mocker.MagicMock()
    response.json.return_value = mock_response

    trx = SendTransactionResponseModel(response=response)

    assert trx.transaction_id == mock_response.get('transactionId')
    assert len(trx.outputs) == 2
    assert trx.outputs[0]['address'] == mock_response.get('outputs')[0]['address']
    assert trx.outputs[0]['amount'] == amount
    assert trx.outputs[1]['amount'] == 0
    assert trx.outputs[1]['opReturnData'] == mock_response.get('outputs')[1]['opReturnData']


def test_send_transaction_response_model_transfer_transaction(mocker: MockerFixture):
    amount = 100000000
    mock_response = {
        'transactionId': generate_transaction_hash(),
        'outputs': [{'address': str(generate_cirrus_address()), 'amount': amount}]
    }

    response = mocker.MagicMock()
    response.json.return_value = mock_response

    trx = SendTransactionResponseModel(response=response)

    assert trx.transaction_id == mock_response.get('transactionId')
    assert len(trx.outputs) == 1
    assert trx.outputs[0]['address'] == mock_response.get('outputs')[0]['address']
    assert trx.outputs[0]['amount'] == amount
