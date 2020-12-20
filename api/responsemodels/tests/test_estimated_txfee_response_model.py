from api.responsemodels import EstimatedTxFeeResponseModel
import pytest
from pytest_mock import MockerFixture
from utilities import Money


def test_estimated_txfee_response_model_large_fee_raises_valueerror(mocker: MockerFixture):
    response = mocker.MagicMock()
    response.json.return_value = 500000000

    with pytest.raises(ValueError):
        EstimatedTxFeeResponseModel(response=response)


def test_estimated_txfee_response_model_reasonable_fee_is_successful(mocker: MockerFixture):
    response = mocker.MagicMock()
    response.json.return_value = 20000

    trx = EstimatedTxFeeResponseModel(response=response)

    assert trx.fee == 20000
    assert isinstance(trx.fee, Money)
    assert str(trx.fee) == '0.00020000'

