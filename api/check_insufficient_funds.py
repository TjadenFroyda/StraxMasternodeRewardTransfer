from exceptions import InsufficientFundsForTransactionException
from .ErrorResponse import ErrorResponse


def check_insufficient_funds(error: ErrorResponse) -> None:
    for message in error.messages:
        if 'Not enough funds to cover the target' in message:
            raise InsufficientFundsForTransactionException('Not enough funds in this address for this transaction.')
