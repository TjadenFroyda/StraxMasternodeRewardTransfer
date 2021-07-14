#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import re
import ast
import argparse
from typing import List, Union, Optional
from binascii import unhexlify
from decouple import config
from datetime import datetime, timedelta
from decimal import Decimal
from pystratis.nodes import CirrusNode
from pystratis.core import Outpoint, Recipient
from pystratis.core.types import Money, Address
from pystratis.api import APIError
from pystratis.api.node.responsemodels import TransactionModel
from pystratis.api.wallet.responsemodels import SpendableTransactionModel, BuildTransactionModel
from pystratis.core.networks import StraxMain, CirrusMain
from credentials import Credentials


MAX_BUILD_ATTEMPTS = 10
HOURS_BETWEEN_CONSOLIDATIONS = 6
SECONDS_PER_HOUR = 3600
WALLETNAME = 'MiningWallet'
CIRRUS_FEDERATION_ADDRESS = Address(address='cYTNBJDbgjRgcKARAvi2UCSsDdyHkjUqJ2', network=CirrusMain())
MAINCHAIN_ADDRESS = Address(address=config('MAINCHAIN_ADDRESS'), network=StraxMain())
SENDING_ADDRESS = Address(address=config('SENDING_ADDRESS'), network=CirrusMain())


def get_spendable_transactions(node: CirrusNode, credentials: Credentials) -> List[SpendableTransactionModel]:
    """Retrieve spendable transactions from the node.

    Args:
        node (CirrusNode): An instance of the cirrus node.
        credentials (Credentials): A Credentials object with wallet information

    Returns:
        List[SpendableTransactionModel]: A list of spendable transactions.
    """
    spendable_transactions = node.wallet.spendable_transactions(wallet_name=credentials.wallet_name)
    spendable_transactions = [x for x in spendable_transactions.transactions]
    return spendable_transactions


def get_spendable_amount(spendable_transactions: List[SpendableTransactionModel]) -> Money:
    """Sums the amount in the spendable transaction list.

    Args:
        spendable_transactions (List[SpendableTransactionModel]): A list of spendable transactions.

    Returns:
        Money: The total spendable amount in the spendable transactions.
    """
    return Money(sum([x.amount.value for x in spendable_transactions]))


def greenlight_transaction(spendable_transactions: List[SpendableTransactionModel], spendable_amount: Money) -> bool:
    """Determine if a cross-chain transaction can be sent.

    Args:
        spendable_transactions (List[SpendableTransactionModel]): A list of spendable transactions.
        spendable_amount (Money): The total spendable amount in the spendable transactions.

    Returns:
        bool: If sending the transaction should get the go-ahead.
    """
    if len(spendable_transactions) < 1:
        print('No mature consolidated transactions found for cross chain transfer.')
        return False
    if spendable_amount < Money('1.0'):
        print('Cannot send transfer than 1 CRS, skipping transfer.')
        return False
    print('Mature consolidated transactions found. Sending transaction to mainchain.')
    return True


def build_transaction_payload(
        credentials: Credentials,
        spendable_transactions: List[SpendableTransactionModel],
        spendable_amount: Money,
        federation_address: Address,
        sending_address: Address,
        mainchain_address: Address,
        fee_amount: Money) -> dict:
    """Build a transaction payload that can be updated later if fee needs to be changed.

    Args:
        credentials (Credentials): A Credentials object with wallet information.
        spendable_transactions (List[SpendableTransactionModel]): A list of spendable transactions.
        spendable_amount (Money): The total spendable amount in the spendable transactions.
        federation_address (Address): The federation address.
        sending_address (Address): The sending address, used as a change address.
        mainchain_address (Address): The mainchain address to be specified as target in the OP_RETURN.
        fee_amount (Money): The fee for the transaction.

    Returns:
        dict: A dictionary containing the processed
    """
    return {
        'credentials': credentials,
        'account_name': 'account 0',
        'outpoints': [Outpoint(transaction_id=x.transaction_id, index=x.index) for x in spendable_transactions],
        'fee_amount': fee_amount,
        'recipients': [Recipient(destination_address=federation_address, subtraction_fee_from_amount=True, amount=spendable_amount)],
        'change_address': sending_address,
        'mainchain_address': mainchain_address
    }


def try_build_transaction(payload: dict) -> Union[BuildTransactionModel, APIError]:
    """Attempt to build a transaction on the node.

    Args:
        payload (dict): A dictionary containing transaction information.

    Returns:
        BuildTransactionModel: If build was successful, a model representing the built transaction.
        APIError: If error was caught, an object with error information.
    """
    try:
        return node.wallet.build_transaction(
            wallet_name=payload['credentials'].wallet_name,
            account_name='account 0',
            password=payload['credentials'].wallet_password,
            outpoints=payload['outpoints'],
            fee_amount=payload['fee_amount'],
            segwit_change_address=False,
            recipients=payload['recipients'],
            allow_unconfirmed=False,
            shuffle_outputs=True,
            change_address=payload['change_address'],
            op_return_data=str(payload['mainchain_address'])
        )
    except APIError as e:
        return e


def try_extract_new_recommended_fee(error_response: APIError) -> Optional[Money]:
    """Tries to extract a new recommended fee from the error message.

    Args:
        error_response (APIError): The APIError object.

    Returns:
        Optional[Money]: The new fee amount, if it could be extracted from the error message.
    """
    recommended_fee_candidates = []
    # Regular expressions for fee extraction.
    policy_minimum = re.compile(r'The policy minimum is \b([0-9]\.[0-9]+)\b')
    fee_minimum = re.compile(r'The minimum fee is \b([0-9]\.[0-9]+)\b')
    errors = ast.literal_eval(error_response.message)['errors']
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
        return recommended_fee
    return None


def inspect_transaction(node: CirrusNode, built_transaction_model: BuildTransactionModel) -> None:
    """Inspect the built transaction by decoding the raw transaction hex and printing the transaction information.
    Args:
        node (CirrusNode): A CirrusNode instance.
        built_transaction_model (BuildTransactionModel): The built transaction for inspection.

    Returns:
        None: Prints the amount being sent, the multisig address, and the mainchain address to stdout.
    """
    print('Simulating transaction. Funds will not be sent.')
    transaction_model: TransactionModel = node.node.decode_raw_transaction(built_transaction_model.hex)
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


def send_transaction(node: CirrusNode, built_transaction_model: BuildTransactionModel):
    """Sends the built transaction and prints the transaction information.

        Args:
            node (CirrusNode): A CirrusNode instance.
            built_transaction_model (BuildTransactionModel): The built transaction for inspection.

        Returns:
            None: Prints the amount being sent, the multisig address, and the mainchain address to stdout.
        """
    send_transaction_model = node.wallet.send_transaction(transaction_hex=built_transaction_model.hex)
    outputs = send_transaction_model.outputs
    for item in outputs:
        if item.amount == Money(0):
            if item.op_return_data is not None:
                print(f"Cross-chain address in OP_RETURN: {item.op_return_data}.")
        else:
            amount_being_sent = item.amount
            receiving_address = item.address
            print(f"Sending {amount_being_sent} to {receiving_address}.")


def print_timeinfo_and_wait(hours_to_wait: int) -> None:
    """Prints current time and next runtime to stdout and then pauses execution.

    Args:
        hours_to_wait (int): The number of hours to wait before returning.

    Returns:
        None: Prints to stdout.
    """
    current_time = datetime.now()
    next_run = (current_time + timedelta(hours=hours_to_wait))
    print(f'Done with consolidation at {current_time:%Y-%m-%d %H:%M}.\nNext run: {next_run:%Y-%m-%d %H:%M}.')
    time.sleep(SECONDS_PER_HOUR * hours_to_wait)


def build_transaction_loop(transaction_payload: dict) -> Union[BuildTransactionModel, bool]:
    """Try to build the transaction. An insufficient fee will cause the build to fail.

        If build fails because of an insufficient fee, the node recommends a new fee from policy.
        This script captures that recommended fee, updates the transaction and tries again.

    Args:
        transaction_payload (dict): A dictionary containing transaction information.

    Returns:
        BuildTransactionModel: If the transaction is built successfully.
        bool: If transaction build fails after MAX_BUILD_ATTEMPTS.
    """
    payload = transaction_payload.copy()
    for _ in range(MAX_BUILD_ATTEMPTS):
        response = try_build_transaction(payload=payload)
        if isinstance(response, BuildTransactionModel):
            return response
        if isinstance(response, APIError):
            if response.code == 400:
                new_fee_amount = try_extract_new_recommended_fee(error_response=response)
                if new_fee_amount is not None:
                    # If fee amount could not be extracted from the error message, assumes another
                    # type of build error occurred and will try to build again with the same fee.
                    payload['fee_amount'] = new_fee_amount
            else:
                # Print other errors and try to build transaction again.
                print(f'Error code {e.code}: {e.message}')
    return False


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--simulate', dest='simulate', default=False, action='store_true', help='Inspect the built transaction without sending.')
    args = parser.parse_args()
    creds = Credentials(wallet_name=WALLETNAME)

    # Obtain the wallet credentials and store them with encryption.
    creds.set_wallet_password()

    node = CirrusNode()
    while True:
        # Get spendable transactions and the total amount.
        spendable_transactions = get_spendable_transactions(node=node, credentials=creds)
        spendable_amount = get_spendable_amount(spendable_transactions)

        # Check to see if criteria for being able to send a cross chain transaction are met.
        if greenlight_transaction(spendable_transactions, spendable_amount):
            transaction_payload = build_transaction_payload(
                credentials=creds,
                spendable_transactions=spendable_transactions,
                spendable_amount=spendable_amount,
                federation_address=CIRRUS_FEDERATION_ADDRESS,
                sending_address=SENDING_ADDRESS,
                mainchain_address=MAINCHAIN_ADDRESS,
                fee_amount=Money('0.00010000')
            )
            # Try to build transaction. If fails after MAX_BUILD_ATTEMPTS, will return False.
            built_transaction = build_transaction_loop(transaction_payload=transaction_payload)

            if built_transaction:
                if args.simulate:
                    inspect_transaction(node=node, built_transaction_model=built_transaction)
                else:
                    send_transaction(node=node, built_transaction_model=built_transaction)
        print_timeinfo_and_wait(hours_to_wait=HOURS_BETWEEN_CONSOLIDATIONS)
