from typing import List
from api import SwaggerAPI
from api.payloads import build_crosschain_transfer_payload
from utilities import Address, Credentials, Network, Outpoint, Money


def transfer(
        credentials: Credentials,
        consolidation_address: Address,
        federation_address: Address,
        mainchain_address: Address,
        min_conf: int,
        max_build_attempts: int,
        simulate: bool = False) -> None:
    """Transfers mature uxto from sidechain to mainchain.

    :param Credentials credentials: Wallet credentials.
    :param Address consolidation_address: The consolidation address.
    :param Address federation_address: The cirrus federation address.
    :param Address mainchain_address: The strax mainchain address.
    :param int min_conf: Requires utxo to have this many confirmations before including in the consolidation transaction.
    :param int max_build_attempts: Number of times to try to find correct fee during transaction build before failing.
    :param bool simulate: Prints the transaction instead of transmitting.
    :return: None
    """
    api = SwaggerAPI()
    spendable_utxos_by_address = api.get_spendable_transactions(
        wallet_name=credentials.wallet_name,
        min_conf=min_conf,
        network=Network.CIRRUS)
    current_address_spendable_utxos: List[Outpoint] = spendable_utxos_by_address.get(str(consolidation_address), [])
    if len(current_address_spendable_utxos) < 1:
        print('No mature consolidated transactions found for cross chain transfer.')
    else:
        print('Mature consolidated transactions found. Sending transaction to mainchain.')
        payload = build_crosschain_transfer_payload(
            outpoints=current_address_spendable_utxos,
            credentials=credentials,
            federation_address=federation_address,
            mainchain_address=mainchain_address,
            change_address=consolidation_address
        )
        if payload.amount < Money(100000000):
            print('Amount in consolidation address less than 1 CRS, skipping transfer.')
        else:
            transaction = api.build_transaction_with_lowest_fee(
                payload=payload,
                crosschain=True,
                num_attempts=max_build_attempts)
            if transaction is not None:
                if simulate:
                    api.inspect_transaction(transaction=transaction)
                else:
                    api.send_transaction(transaction=transaction)
