from typing import Union
from utilities import Money
from exceptions import RecommendedFeeTooHighException, NodeResponseException, FeeTooLowException
from .ErrorResponse import ErrorResponse


def recommended_fee_sanity_check(recommended_fee: Union[Money, None], error: ErrorResponse) -> None:
    """Sanity check for the recommended fee.

    :param Union[Money, None] recommended_fee: The recommended fee.
    :param ErrorResponse error: The error response.
    :return: None
    :raises NodeResponseException: If invalid password given.
    :raises RecommendedFeeTooHighException: If the recommended fee is more than 1 CRS.
    :raises FeeTooLowException: If the current fee was too small per network policy.
    """
    if recommended_fee is None:
        raise NodeResponseException(
            message='Error building transaction.',
            response=str(error.json))
    if recommended_fee >= Money(100000000):
        raise RecommendedFeeTooHighException(
            message=f'Recommended fee size more than 1 CRS. Recommended fee size: {recommended_fee}',
            fee=recommended_fee)
    raise FeeTooLowException(
        message=f'Fee size too small per network policy. Recommended fee size: {recommended_fee}',
        fee=recommended_fee)
