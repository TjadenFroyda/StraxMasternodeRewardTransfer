from api.payloads import TransactionPayload
from exceptions import FeeTooLowException, RecommendedFeeTooHighException, NodeResponseException


def send_batched_payload(
        payload: TransactionPayload,
        crosschain: bool,
        num_attempts: int,
        simulate: bool = True) -> None:
    """Builds and sends a batched transaction.

    :param TransactionPayload payload: A TransactionPayload
    :param bool crosschain: If the transaction is crosschain.
    :param int num_attempts: The maximum number of attempts to try to find a valid fee amount.
    :param bool simulate: Print the transaction instead of sending. Default: True
    :return: None
    """
    from . import send_transaction, inspect_raw_transaction, build_transaction
    transaction_payload = payload

    # The loop is only repeated if the fee is too low.
    for _ in range(num_attempts):

        try:
            transaction = build_transaction(payload=transaction_payload, crosschain=crosschain)
            if simulate:
                print('Simulating transaction.')
                raw = inspect_raw_transaction(transaction)
                print(f'Hex: {raw.hex}')
                print(f'Vin: {raw.vin}')
                print(f'Vout: {raw.vout}')
            else:
                response = send_transaction(transaction)
                print(response)
        except FeeTooLowException as e:
            print(f'Updating fee to {e.recommended_fee}.')
            transaction_payload.fee_amount = e.recommended_fee
            continue
        except RecommendedFeeTooHighException as e:
            print(e.message)
        except NodeResponseException as e:
            print(e.message)
            print(e.response)
        break
