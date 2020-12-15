from api.responsemodels import BuildTransactionResponseModel, InspectTransactionResponseModel
from exceptions import NodeResponseException
import json
import requests as req
from .ErrorResponse import ErrorResponse


def inspect_transaction(
        uri: str,
        transaction: BuildTransactionResponseModel) -> None:
    """Decodes a raw hex transaction through the decoderawtransaction api endpoint.

    :param str uri: The uri.
    :param BuildTransactionResponseModel transaction: A BuildTransactionResponseModel.
    :return: The node response.
    :rtype: InspectTransactionResponseModel
    :raises NodeResponseException: If HTTP post request not successful.
    """
    headers = {'Accept': '*/*', 'Content-Type': 'application/json'}
    data = {'rawHex': transaction.hex}
    res = req.post(
        url=uri,
        data=json.dumps(data),
        headers=headers)
    if res.status_code == 200:
        print('Simulating transaction.')
        raw = InspectTransactionResponseModel(res)
        print(f'Hex: {raw.hex}')
        print(f'Vin: {raw.vin}')
        print(f'Vout: {raw.vout}')
    else:
        error = ErrorResponse(res)
        raise NodeResponseException(message='Error inspecting transaction.', response=str(error.json))
