from utilities import Money
from api.responsemodels import BuildTransactionResponseModel
from .generators import generate_transaction_hash, generate_hexstring
import pytest
from pytest_mock import MockerFixture


def test_build_transaction_response_model_fee_in_satoshis_is_successful(mocker: MockerFixture):
    response = mocker.MagicMock()
    response.json.return_value = {'transactionId': generate_transaction_hash(), 'hex': generate_hexstring(), 'fee': 10000}

    trx = BuildTransactionResponseModel(response)

    assert trx.fee == 10000
    assert isinstance(trx.fee, Money)
    assert str(trx.fee) == '0.00010000'


def test_build_transaction_response_model_float_fee_raises_valueerror(mocker: MockerFixture):
    response = mocker.MagicMock()
    response.json.return_value = {'transactionId': generate_transaction_hash(), 'hex': generate_hexstring(), 'fee': 0.00010000}

    with pytest.raises(ValueError):
        BuildTransactionResponseModel(response=response)

    with pytest.raises(ValueError):
        response.json.return_value = {'transactionId': generate_transaction_hash(), 'hex': generate_hexstring(), 'fee': 10000.0}
        BuildTransactionResponseModel(response=response)

