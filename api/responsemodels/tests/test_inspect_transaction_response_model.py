from pytest_mock import MockerFixture
from api.responsemodels import InspectTransactionResponseModel
from .generators import generate_transaction_hash, generate_hexstring


def test_inspect_transaction_response_model(mocker: MockerFixture):
    mock_raw_transaction = {
        'txid': generate_transaction_hash(),
        'hex': generate_hexstring(),
        'hash': generate_transaction_hash(),
        'version': 0,
        'size': 1,
        'vsize': 1,
        'weight': 1,
        'locktime': 1,
        'vin': [],
        'vout': []
    }
    response = mocker.MagicMock()
    response.json.return_value = mock_raw_transaction

    trx = InspectTransactionResponseModel(response=response)

    assert trx.transaction_id == mock_raw_transaction['txid']
    assert trx.hex == mock_raw_transaction['hex']
