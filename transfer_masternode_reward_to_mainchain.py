#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import re
import ast
import argparse
from binascii import unhexlify
from decouple import config
from datetime import datetime, timedelta
from decimal import Decimal
from pystratis.nodes import CirrusNode
from pystratis.core import Outpoint, Recipient
from pystratis.core.types import Money, Address
from pystratis.api import APIError
from pystratis.api.node.responsemodels import TransactionModel
from pystratis.core.networks import StraxMain, CirrusMain
from credentials import Credentials


MAX_BUILD_ATTEMPTS = 10
HOURS_BETWEEN_CONSOLIDATIONS = 6
SECONDS_PER_HOUR = 3600
WALLETNAME = 'MiningWallet'
CIRRUS_FEDERATION_ADDRESS = Address(address='cYTNBJDbgjRgcKARAvi2UCSsDdyHkjUqJ2', network=CirrusMain())
MAINCHAIN_ADDRESS = Address(address=config('MAINCHAIN_ADDRESS'), network=StraxMain())
SENDING_ADDRESS = Address(address=config('SENDING_ADDRESS'), network=CirrusMain())


def transfer(
        credentials: Credentials,
        sending_address: Address,
        federation_address: Address,
        mainchain_address: Address,
        max_build_attempts: int,
        simulate: bool
) -> None:
    """Transfers mature uxto from sidechain to specified mainchain address.

    Args:
        credentials (Credentials): Wallet credentials.
        sending_address (Address): The consolidation address.
        federation_address (Address): The cirrus federation address.
        mainchain_address (Address): The strax mainchain address.
        max_build_attempts (int): Number of times to try to find correct fee during transaction build before failing.
        simulate (bool): Prints the transaction instead of transmitting. Default=False. (cmdline arg '--simulate')

    Returns:
        None
    """
    node = CirrusNode()
    # Retrieve spendable transactions from the node
    s_txs = node.wallet.spendable_transactions(wallet_name=credentials.wallet_name)
    s_txs = [x for x in s_txs.transactions]

    # Determine the amount that is transferable.
    s_txs_amount = Money(sum([x.amount.value for x in s_txs]))

    if len(s_txs) < 1:
        print('No mature consolidated transactions found for cross chain transfer.')
    elif s_txs_amount < Money('1.0'):
        print('Cannot send transfer than 1 CRS, skipping transfer.')
    else:
        print('Mature consolidated transactions found. Sending transaction to mainchain.')
        fee_amount = Money('0.00010000')
        for _ in range(max_build_attempts):
            try:
                payload = node.wallet.build_transaction(
                    wallet_name=credentials.wallet_name,
                    account_name='account 0',
                    password=credentials.wallet_password,
                    outpoints=[Outpoint(transaction_id=x.transaction_id, index=x.index) for x in s_txs],
                    fee_amount=fee_amount,
                    segwit_change_address=False,
                    recipients=[Recipient(destination_address=federation_address, subtraction_fee_from_amount=True, amount=s_txs_amount)],
                    allow_unconfirmed=False,
                    shuffle_outputs=True,
                    change_address=sending_address,
                    op_return_data=str(mainchain_address)
                )
                if simulate:
                    print('Simulating transaction. Funds will not be sent.')
                    transaction_model: TransactionModel = node.node.decode_raw_transaction(payload.hex)
                    model_dict = transaction_model.dict()
                    for item in model_dict['vout']:
                        if item['value'] == Money(0):
                            # Retreive the op_return field
                            op_return_data = item['script_pubkey']['asm']

                            # The hex-encoded destination address is the second portion of the OP_RETURN.
                            # We need to split the data at the space, unhexify, and decode to utf-8.
                            op_return_address = unhexlify(op_return_data.split(' ')[1]).decode('utf-8')
                            print(f"Cross-chain address in OP_RETURN: {op_return_address}.")
                        else:
                            # Validate that the correct amount is being sent to the federation multisig address.
                            amount_being_sent = item['value']
                            receiving_address = item['script_pubkey']['addresses'][0]
                            print(f"Sending {amount_being_sent} to {receiving_address}.")
                else:
                    send_transaction_model = node.wallet.send_transaction(transaction_hex=payload.hex)
                    outputs = send_transaction_model.outputs
                    for item in outputs:
                        if item.amount == Money(0):
                            op_return_data = item.op_return_data
                            if op_return_data is not None:
                                op_return_address = unhexlify(op_return_data.split(' ')[1]).decode('utf-8')
                                print(f"Cross-chain address in OP_RETURN: {op_return_address}.")
                        else:
                            amount_being_sent = item.amount
                            receiving_address = item.address
                            print(f"Sending {amount_being_sent} to {receiving_address}.")
                # Break on success.
                break
            except APIError as e:
                # Try to extract the recommended fee from the error message.
                if e.code == 400:
                    recommended_fee_candidates = []
                    # Regular expressions for fee extraction.
                    policy_minimum = re.compile(r'The policy minimum is \b([0-9]\.[0-9]+)\b')
                    fee_minimum = re.compile(r'The minimum fee is \b([0-9]\.[0-9]+)\b')
                    errors = ast.literal_eval(e.message)['errors']

                    for error in errors:
                        print(f"Error code {error['status']}: {error['message']}")
                        # If the fee cannot be extracted from the message using the regex, nothing will be added to the list.
                        recommended_fee_candidates.extend([Money(x) for x in policy_minimum.findall(error['message'])])
                        recommended_fee_candidates.extend([Money(x) for x in fee_minimum.findall(error['message'])])

                    if len(recommended_fee_candidates) > 0:
                        # Choose the largest fee extracted as the next fee.
                        recommended_fee = max(recommended_fee_candidates)
                        # Sanity check for recommended fee candidate.
                        if recommended_fee > Money(0.1):
                            raise ValueError('New fee amount should not be greater than 0.1 CRS')
                        print(f'Updating fee to: {recommended_fee}')
                        fee_amount = recommended_fee
                else:
                    print(f'Error code {e.code}: {e.message}')


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--simulate', dest='simulate', default=False, action='store_true', help='Inspect the built transaction without sending.')
    args = parser.parse_args()
    creds = Credentials(wallet_name=WALLETNAME)
    creds.set_wallet_password()

    while True:
        transfer(
            credentials=creds,
            sending_address=SENDING_ADDRESS,
            federation_address=CIRRUS_FEDERATION_ADDRESS,
            mainchain_address=MAINCHAIN_ADDRESS,
            max_build_attempts=MAX_BUILD_ATTEMPTS,
            simulate=args.simulate
        )
        current_time = datetime.now()
        next_run = (current_time + timedelta(hours=HOURS_BETWEEN_CONSOLIDATIONS))
        print(f'Done with consolidation at {current_time:%Y-%m-%d %H:%M}.\nNext run: {next_run:%Y-%m-%d %H:%M}.')
        time.sleep(SECONDS_PER_HOUR * HOURS_BETWEEN_CONSOLIDATIONS)
