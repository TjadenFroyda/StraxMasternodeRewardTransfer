import json
import requests as req
from api.responsemodels import BuildTransactionResponseModel
from .ErrorResponse import ErrorResponse
from .check_invalid_password import check_invalid_password
from .recommended_fee_sanity_check import recommended_fee_sanity_check
from .try_extract_policy_minimum_from_error_message import try_extract_policy_minimum_from_error_message


def build_transaction(
        uri: str,
        payload: dict) -> BuildTransactionResponseModel:
    """Builds the transaction using the node api.

    :param str uri: The build_transaction uri.
    :param dict payload: A payload dict.
    :return: A dictionary representing the built transaction.
    :rtype: BuildTransactionResponseModel
    :raises NodeResponseException: If invalid password given.
    :raises RecommendedFeeTooHighException: If the recommended fee is more than 1 CRS.
    :raises FeeTooLowException: If the current fee was too small per network policy.
    """
    headers = {'Accept': '*/*', 'Content-Type': 'application/json'}
    res = req.post(
        url=uri,
        data=json.dumps(payload),
        headers=headers)
    if res.status_code == 200:
        return BuildTransactionResponseModel(response=res)
    if res.status_code == 400:
        error = ErrorResponse(response=res)
        check_invalid_password(error)
        recommended_fee = try_extract_policy_minimum_from_error_message(error=error)
        recommended_fee_sanity_check(recommended_fee=recommended_fee, error=error)
