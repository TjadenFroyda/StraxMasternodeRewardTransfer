from typing import List
from utilities import Outpoint, Credentials, Network, Recipient, Money, Address
from .TransactionPayload import TransactionPayload


def build_crosschain_transfer_payload(
        outpoints: List[Outpoint],
        credentials: Credentials,
        federation_address: Address,
        mainchain_address: Address,
        change_address: Address,
        fee: Money = Money(10000)) -> TransactionPayload:
    """Builds a crosschain transfer payload.

    :param List[Outpoint] outpoints: The outpoints to include in the transaction.
    :param Credentials credentials: The credentials for signing the transaction.
    :param Address federation_address: The federation address.
    :param Address mainchain_address: The mainchain address.
    :param Address change_address: The change address (usually sender address).
    :param Money fee: The fee
    :return: A transaction payload.
    :rtype: TransactionPayload
    """
    # Build payload first
    payload = TransactionPayload(network=Network.CIRRUS)
    payload.outpoints = outpoints
    recipients = [Recipient(network=Network.CIRRUS, item={'destinationAddress': federation_address})]
    payload.recipients = recipients
    payload.fee_amount = fee
    payload.segwit_change_address = False
    payload.wallet_name = credentials.wallet_name
    payload.password = credentials.wallet_password
    payload.account_name = 'account 0'
    payload.opreturn_data = mainchain_address
    payload.allow_unconfirmed = True
    payload.shuffle_outputs = False
    payload.change_address = change_address

    return payload
