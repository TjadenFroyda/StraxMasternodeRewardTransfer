from api.payloads import TransactionPayload
from api.responsemodels import EstimatedTxFeeResponseModel
from exceptions import InsufficientFundsForTransactionException, NodeResponseException
import json
import requests as req


def get_estimated_txfee(
        payload: TransactionPayload,
        crosschain: bool) -> EstimatedTxFeeResponseModel:
    """Calls the estimate-txfee api endpoint to calculate the transaction fee.

    :param TransactionPayload payload: An instance of TransactionPayload.
    :param bool crosschain: If transaction is being sent crosschain.
    :return: The estimated fee for this transaction.
    :rtype: EstimatedTxFeeResponseModel
    :raises NodeResponseException: If HTTP post request not successful.
    :raises InsufficientFundsForTransactionException: If not enough funds in the address for the transaction.
    """
    from . import SwaggerAPI
    api = SwaggerAPI()
    uri = f'{api.base_uri}/Wallet/estimate-txfee'
    res = req.post(uri, data=json.dumps(payload.get_estimate_txfee_payload(crosschain=crosschain)), headers=api.headers)
    if res.status_code == 200:
        return EstimatedTxFeeResponseModel(res)
    if res.status_code == 400:
        message = EstimatedTxFeeResponseModel(res).errors[0].get('message')
        if 'Not enough funds to cover the target' in message:
            raise InsufficientFundsForTransactionException('Not enough funds in this address for this transaction.')
    raise NodeResponseException(message='Error estimating transaction fee.', response=res.json())
