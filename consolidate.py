from more_itertools import chunked
from api import SwaggerAPI
from api.payloads import build_consolidation_transaction_payload
from utilities import Address, Credentials, Network


def consolidate(
        credentials: Credentials,
        consolidation_address: Address,
        batch_size: int = 64,
        min_conf: int = 0,
        max_build_attempts: int = 10,
        simulate: bool = False) -> None:
    """Consolidates spendable utxo in the wallet into a single destination address.

    :param Credentials credentials: Wallet credentials.
    :param Address consolidation_address: The consolidation address.
    :param int batch_size: The batch size for consolidation.
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
    print('Searching for spendable uxtos to consolidate.')
    for address in spendable_utxos_by_address.keys():
        if address == str(consolidation_address):
            continue
        current_address_spendable_utxos = spendable_utxos_by_address.get(address)
        total_amount_in_address = sum([int(utxo.amount) for utxo in current_address_spendable_utxos])
        print(f'Consolidating {address} with {len(current_address_spendable_utxos)} utxos. Total: {total_amount_in_address}.')
        for batch in chunked(current_address_spendable_utxos, batch_size):
            payload = build_consolidation_transaction_payload(
                outpoints=batch,
                credentials=credentials,
                destination_address=consolidation_address)
            transaction = api.build_transaction_with_lowest_fee(
                payload=payload,
                crosschain=False,
                num_attempts=max_build_attempts)
            if transaction is not None:
                if simulate:
                    api.inspect_transaction(transaction=transaction)
                else:
                    api.send_transaction(transaction=transaction)
