from api.payloads import TransactionPayload
from api.responsemodels import BuildTransactionResponseModel, EstimatedTxFeeResponseModel
from exceptions import FeeTooLowException, RecommendedFeeTooHighException, NodeResponseException
from typing import Union
from utilities import Network
from .aggregate_spendable_utxos_by_address import aggregate_spendable_utxos_by_address
from .build_transaction import build_transaction
from .inspect_transaction import inspect_transaction
from .get_estimated_txfee import get_estimated_txfee
from .send_transaction import send_transaction


class SwaggerAPI:
    def __init__(self):
        self.base_uri = 'http://localhost:37223/api'

    def _get_build_transaction_uri(self):
        return f'{self.base_uri}/Wallet/build-transaction'

    def _get_spendable_transactions_uri(self,
                                        wallet_name: str,
                                        min_conf: int):
        return f'{self.base_uri}/Wallet/spendable-transactions?WalletName={wallet_name}&MinConfirmations={min_conf}'

    def _get_decode_raw_transaction_uri(self):
        return f'{self.base_uri}/Node/decoderawtransaction'

    def _get_send_transaction_uri(self):
        return f'{self.base_uri}/Wallet/send-transaction'

    def _get_estimate_txfee_uri(self):
        return f'{self.base_uri}/Wallet/estimate-txfee'

    def build_transaction(self,
                          payload: TransactionPayload,
                          crosschain: bool) -> BuildTransactionResponseModel:
        """Builds a transaction.

        :param TransactionPayload payload: A transaction payload.
        :param bool crosschain: If this is a crosschain transaction.
        :return: The built transaction.
        :rtype: BuildTransactionResponseModel
        """
        payload: dict = payload.get_build_transaction_payload(crosschain=crosschain)
        return build_transaction(
            uri=self._get_build_transaction_uri(),
            payload=payload
        )

    def get_spendable_transactions(self,
                                   wallet_name: str,
                                   min_conf: int,
                                   network: Network) -> dict:
        """Retrieves a list of spendable transactions from the specified wallet with minimum confirmations.

        :param str wallet_name: The wallet name.
        :param int min_conf: Include only utxo with at least this many confirmations.
        :param Network network: The network the transaction is being sent on.
        :return: Spendable transactions.
        :rtype: dict
        """
        return aggregate_spendable_utxos_by_address(
            uri=self._get_spendable_transactions_uri(wallet_name=wallet_name, min_conf=min_conf),
            network=network
        )

    def get_estimated_txfee(self,
                            payload: TransactionPayload,
                            crosschain: bool) -> EstimatedTxFeeResponseModel:
        """Retrieves the estimated transaction fee.

        :param TransactionPayload payload: A transaction payload.
        :param bool crosschain: If this is a crosschain transaction.
        :return: The estimated fee
        :rtype: EstimatedTxFeeResponseModel
        """
        payload: dict = payload.get_estimate_txfee_payload(crosschain=crosschain)
        return get_estimated_txfee(
            uri=self._get_estimate_txfee_uri(),
            payload=payload
        )

    def inspect_transaction(self,
                            transaction: BuildTransactionResponseModel) -> None:
        """Prints a transaction to stdout.

        :param BuildTransactionResponseModel transaction:
        :return: None
        :rtype: None
        """
        return inspect_transaction(
            uri=self._get_decode_raw_transaction_uri(),
            transaction=transaction
        )

    def send_transaction(self,
                         transaction: BuildTransactionResponseModel) -> None:
        """Broadcasts a signed transaction to the network.

        :param BuildTransactionResponseModel transaction:
        :return: None
        :rtype: None
        """
        return send_transaction(
            uri=self._get_send_transaction_uri(),
            transaction=transaction
        )

    def build_transaction_with_lowest_fee(self,
                                          payload: TransactionPayload,
                                          crosschain: bool,
                                          num_attempts: int) -> Union[BuildTransactionResponseModel, None]:
        """Attempts to build the transaction with the lowest fee.

        :param TransactionPayload payload: A TransactionPayload
        :param bool crosschain: If the transaction is crosschain.
        :param int num_attempts: The maximum number of attempts to try to find a valid fee amount.
        :return: The built transaction.
        :rtype: Union[BuildTransactionResponseModel, None]
        """
        transaction_payload: TransactionPayload = payload
        for _ in range(num_attempts):
            try:
                payload_dict = transaction_payload.get_build_transaction_payload(crosschain=crosschain)
                return build_transaction(
                    uri=self._get_build_transaction_uri(),
                    payload=payload_dict)
            except FeeTooLowException as e:
                print(f'Updating fee to {e.recommended_fee}.')
                transaction_payload.fee_amount = e.recommended_fee
                continue
            except RecommendedFeeTooHighException as e:
                print(e.message)
            except NodeResponseException as e:
                print(e.message)
                print(e.response)
        return None
