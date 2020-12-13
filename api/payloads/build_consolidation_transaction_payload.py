from typing import List
from utilities import Outpoint, Credentials, Network, Recipient, Money, Address
from . import TransactionPayload


def build_consolidation_transaction_payload(
        outpoints: List[Outpoint],
        credentials: Credentials,
        destination_address: Address,
        fee: Money = Money(10000)) -> TransactionPayload:
    """Builds a consolidation transaction payload.

    :param List[Outpoint] outpoints: The outpoints to include in the transaction.
    :param Credentials credentials: The credentials for signing the transaction.
    :param Address destination_address: The destination address
    :param Money fee: The fee
    :return: A transaction payload.
    :rtype: TransactionPayload
    """
    # Build payload first.
    payload = TransactionPayload(network=Network.CIRRUS)
    payload.outpoints = outpoints
    recipients = [Recipient(network=Network.CIRRUS, item={'destinationAddress': destination_address})]
    payload.recipients = recipients
    payload.fee_amount = fee
    payload.segwit_change_address = False
    payload.wallet_name = credentials.wallet_name
    payload.password = credentials.wallet_password
    payload.account_name = 'account 0'
    payload.allow_unconfirmed = True
    payload.shuffle_outputs = False
    payload.change_address = destination_address

    # Get fee estimate and update amounts.
    from api import get_estimated_txfee
    estimated_fee = get_estimated_txfee(payload=payload, crosschain=False)
    payload.fee_amount = estimated_fee.fee
    return payload
