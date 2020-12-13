from api.responsemodels import BuildTransactionResponseModel, InspectRawTransactionResponseModel
from exceptions import NodeResponseException
import json
import requests as req


def inspect_raw_transaction(
        transaction: BuildTransactionResponseModel) -> InspectRawTransactionResponseModel:
    """Decodes a raw hex transaction through the decoderawtransaction api endpoint.

    :param BuildTransactionResponseModel transaction: A BuildTransactionResponseModel.
    :return: The node response.
    :rtype: InspectRawTransactionResponseModel
    :raises NodeResponseException: If HTTP post request not successful.
    """
    from . import SwaggerAPI
    api = SwaggerAPI()
    uri = f'{api.base_uri}/Node/decoderawtransaction'
    data = {'rawHex': transaction.hex}
    res = req.post(uri, data=json.dumps(data), headers=api.headers)
    if res.status_code == 200:
        return InspectRawTransactionResponseModel(res)
    raise NodeResponseException(message='Error inspecting transaction.', response=res.json())
