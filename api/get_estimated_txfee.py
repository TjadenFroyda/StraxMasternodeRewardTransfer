from api.responsemodels import EstimatedTxFeeResponseModel
from exceptions import NodeResponseException
import json
import requests as req
from .ErrorResponse import ErrorResponse
from .check_insufficient_funds import check_insufficient_funds


def get_estimated_txfee(
        uri: str,
        payload: dict) -> EstimatedTxFeeResponseModel:
    """Calls the estimate-txfee api endpoint to calculate the transaction fee.

    :param str uri: The uri.
    :param dict payload: An instance of TransactionPayload.
    :return: The estimated fee for this transaction.
    :rtype: EstimatedTxFeeResponseModel
    :raises NodeResponseException: If HTTP post request not successful.
    :raises InsufficientFundsForTransactionException: If not enough funds in the address for the transaction.
    """
    headers = {'Accept': '*/*', 'Content-Type': 'application/json'}
    res = req.post(
        url=uri,
        data=json.dumps(payload),
        headers=headers)
    if res.status_code == 200:
        return EstimatedTxFeeResponseModel(res)
    if res.status_code == 400:
        error = ErrorResponse(response=res)
        check_insufficient_funds(error)
        raise NodeResponseException(message='Error estimating transaction fee.', response=str(error.json))
