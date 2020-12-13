from api.responsemodels import SpendableTransactionsResponseModel
from collections import defaultdict
from exceptions import NodeResponseException
import requests as req
from utilities import Network


def aggregate_spendable_utxos_by_address(
        wallet_name: str,
        min_conf: int,
        network: Network) -> dict:
    """Retreives a list of spendable utxos from the wallet with at least min_conf confirmations.

    :param str wallet_name: The wallet name.
    :param int min_conf: Minimum number of confirmations.
    :param Network network: The network the transaction is being sent on.
    :return: A list of spendable transactions from the wallet meeting the minimum confirmation threshold, organized by address.
    :rtype: dict
    :raises NodeResponseException: If HTTP get request not successful.
    """
    from . import SwaggerAPI
    api = SwaggerAPI()
    uri = f'{api.base_uri}/Wallet/spendable-transactions?WalletName={wallet_name}&MinConfirmations={min_conf}'
    res = req.get(uri)
    if res.status_code == 200:
        utxos = SpendableTransactionsResponseModel(network=network, response=res)
        utxos_by_address = defaultdict(list)
        for utxo in utxos.spendable:
            utxos_by_address[str(utxo.address)].append(utxo)
        return dict(utxos_by_address)
    raise NodeResponseException(message='Error retrieving spendable transactions.', response=res.json())
