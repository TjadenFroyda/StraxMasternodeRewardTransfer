from api.responsemodels import BuildTransactionResponseModel, SendTransactionResponseModel
from exceptions import NodeResponseException
import json
import requests as req


def send_transaction(
        transaction: BuildTransactionResponseModel) -> SendTransactionResponseModel:
    """Broadcasts a signed transaction to the network.

    :param BuildTransactionResponseModel transaction: A BuildTransactionResponseModel.
    :return: The node response.
    :rtype: SendTransactionResponseModel
    :raises NodeResponseException: If HTTP post request not successful.
    """
    from . import SwaggerAPI
    api = SwaggerAPI()
    uri = f'{api.base_uri}/Wallet/send-transaction'
    data = {'hex': transaction.hex}
    res = req.post(uri, data=json.dumps(data), headers=api.headers)
    if res.status_code == 200:
        return SendTransactionResponseModel(res)
    raise NodeResponseException(message='Error sending transaction.', response=res.json())
