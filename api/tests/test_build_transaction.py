import pytest
from pytest_mock import MockerFixture
from api import SwaggerAPI
from api.responsemodels import BuildTransactionResponseModel
from exceptions import NodeResponseException, RecommendedFeeTooHighException, FeeTooLowException
from .generators import generate_transaction_hash, generate_hexstring


def test_build_transaction_is_successful(mocker: MockerFixture):
    payload = mocker.MagicMock()
    payload.get_build_transaction_payload.return_value = {'dummy': 'values'}
    response = mocker.MagicMock(status_code=200)
    response.json.return_value = {'transactionId': generate_transaction_hash(), 'hex': generate_hexstring(), 'fee': 10000}
    mocker.patch('requests.post', return_value=response)
    api = SwaggerAPI()

    response = api.build_transaction(payload=payload, crosschain=True)

    assert isinstance(response, BuildTransactionResponseModel)


def test_build_transaction_raises_noderesponseexception_for_invalid_password(mocker: MockerFixture):
    payload = mocker.MagicMock()
    payload.get_build_transaction_payload.return_value = {'dummy': 'values'}
    response = mocker.MagicMock(status_code=400)
    response.json.return_value = {'errors': [{'message': 'Invalid password (or invalid Network)'}]}
    mocker.patch('requests.post', return_value=response)
    api = SwaggerAPI()

    with pytest.raises(NodeResponseException):
        api.build_transaction(payload=payload, crosschain=False)


def test_build_transaction_raises_noderesponseexception_general_error(mocker: MockerFixture):
    payload = mocker.MagicMock()
    payload.get_build_transaction_payload.return_value = {'dummy': 'values'}
    response = mocker.MagicMock(status_code=400)
    response.json.return_value = {'errors': [{'message': 'General error'}]}
    mocker.patch('requests.post', return_value=response)
    api = SwaggerAPI()

    with pytest.raises(NodeResponseException) as ctx:
        api.build_transaction(payload=payload, crosschain=False)
        assert ctx.value.message == 'Error building crosschain transaction.'


def test_build_transaction_raises_recommended_fee_too_high_exception(mocker: MockerFixture):
    payload = mocker.MagicMock()
    payload.get_build_transaction_payload.return_value = {'dummy': 'values'}
    response = mocker.MagicMock(status_code=400)
    response.json.return_value = {'errors': [{'message': 'The policy minimum is 5.0.'}]}
    mocker.patch('requests.post', return_value=response)
    api = SwaggerAPI()

    with pytest.raises(RecommendedFeeTooHighException) as ctx:
        api.build_transaction(payload=payload, crosschain=False)
    assert ctx.value.fee == int(5.0 * 1e8)


def test_build_transaction_raises_fee_too_low_exception(mocker: MockerFixture):
    payload = mocker.MagicMock()
    payload.get_build_transaction_payload.return_value = {'dummy': 'values'}
    response = mocker.MagicMock(status_code=400)
    response.json.return_value = {'errors': [{'message': 'The policy minimum is 0.00012345.'}]}
    mocker.patch('requests.post', return_value=response)
    api = SwaggerAPI()

    with pytest.raises(FeeTooLowException) as ctx:
        api.build_transaction(payload=payload, crosschain=False)
    assert ctx.value.recommended_fee == 12345
