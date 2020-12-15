from api.responsemodels import SpendableTransactionsResponseModel
from collections import defaultdict
from exceptions import NodeResponseException
import requests as req
from utilities import Network
from .ErrorResponse import ErrorResponse


def aggregate_spendable_utxos_by_address(
        uri: str,
        network: Network) -> dict:
    """Retreives a list of spendable utxos from the wallet with at least min_conf confirmations.

    :param str uri: The uri.
    :param Network network: The network the transaction is being sent on.
    :return: A list of spendable transactions from the wallet meeting the minimum confirmation threshold, organized by address.
    :rtype: dict
    :raises NodeResponseException: If HTTP get request not successful.
    """
    res = req.get(url=uri)
    if res.status_code == 200:
        utxos = SpendableTransactionsResponseModel(network=network, response=res)
        utxos_by_address = defaultdict(list)
        for utxo in utxos.spendable:
            utxos_by_address[str(utxo.address)].append(utxo)
        return dict(utxos_by_address)
    else:
        error = ErrorResponse(res)
        raise NodeResponseException(message='Error retrieving spendable transactions.', response=str(error.json))
