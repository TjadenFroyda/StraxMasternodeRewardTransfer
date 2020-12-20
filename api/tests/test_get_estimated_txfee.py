import pytest
from pytest_mock import MockerFixture
from api import SwaggerAPI
from api.responsemodels import EstimatedTxFeeResponseModel
from exceptions import InsufficientFundsForTransactionException, NodeResponseException


def test_estimated_txfee_is_successful(mocker: MockerFixture):
    payload = mocker.MagicMock()
    payload.get_estimate_txfee_payload.return_value = {'dummy': 'values'}
    response = mocker.MagicMock(status_code=200)
    response.json.return_value = 20000
    mocker.patch('requests.post', return_value=response)
    api = SwaggerAPI()

    response = api.get_estimated_txfee(payload=payload, crosschain=True)

    assert isinstance(response, EstimatedTxFeeResponseModel)
    assert response.fee == 20000


def test_estimated_txfee_raises_insufficient_funds_exception(mocker: MockerFixture):
    payload = mocker.MagicMock()
    payload.get_estimate_txfee_payload.return_value = {'dummy': 'values'}
    response = mocker.MagicMock(status_code=400)
    response.json.return_value = {'errors': [{'message': 'Not enough funds to cover the target at address'}]}
    mocker.patch('requests.post', return_value=response)
    api = SwaggerAPI()

    with pytest.raises(InsufficientFundsForTransactionException):
        api.get_estimated_txfee(payload=payload, crosschain=False)


def test_estimated_txfee_raises_noderesponseexception(mocker: MockerFixture):
    payload = mocker.MagicMock()
    payload.get_estimate_txfee_payload.return_value = {'dummy': 'values'}
    response = mocker.MagicMock(status_code=400)
    response.json.return_value = {'errors': [{'message': 'Some other message goes here.'}]}
    mocker.patch('requests.post', return_value=response)
    api = SwaggerAPI()

    with pytest.raises(NodeResponseException):
        api.get_estimated_txfee(payload=payload, crosschain=False)
