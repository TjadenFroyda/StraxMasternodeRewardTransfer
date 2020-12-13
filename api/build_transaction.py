from api.payloads import TransactionPayload
from api.responsemodels import BuildTransactionResponseModel
from exceptions import NodeResponseException, RecommendedFeeTooHighException, FeeTooLowException
import json
import re
import requests as req
from utilities import Money


def build_transaction(
        payload: TransactionPayload,
        crosschain: bool) -> BuildTransactionResponseModel:
    """Builds the transaction using the node api.

    :param TransactionPayload payload: An instance of TransactionPayload.
    :param bool crosschain: If the transaction is being send crosschain.
    :return: A dictionary representing the built transaction.
    :rtype: BuildTransactionResponseModel
    :raises NodeResponseException: If HTTP post request not successful.
    :raises NodeResponseException: If invalid password given.
    :raises RecommendedFeeTooHighException: If the recommended fee is more than 1 CRS.
    :raises FeeTooLowException: If the current fee was too small per network policy.
    """
    from . import SwaggerAPI
    api = SwaggerAPI()
    uri = f'{api.base_uri}/Wallet/build-transaction'
    res = req.post(uri, data=json.dumps(payload.get_build_transaction_payload(crosschain=crosschain)), headers=api.headers)
    if res.status_code == 200:
        return BuildTransactionResponseModel(res)
    if res.status_code == 400:
        message = BuildTransactionResponseModel(res).errors[0].get('message')

        if message == 'Invalid password (or invalid Network)':
            raise NodeResponseException(message='Invalid password.', response=res.json())

        # Try to extract the policy minimum recommended by the node's error message.
        try:
            r_policy = re.compile(r'The policy minimum is \b([0-9]\.[0-9]+)\b')
            recommended_fee = Money(int(max([float(x) * 1e8 for x in r_policy.findall(message)])))
        except ValueError:
            raise NodeResponseException(message='Error building transaction.', response=res.json())

        # Fee sanity check (in satoshis).
        if recommended_fee >= 100000000:
            raise RecommendedFeeTooHighException(
                f'Recommended fee size more than 1 CRS. Recommended fee size: {recommended_fee}',
                fee=recommended_fee)

        # Raise exception with the suggested fee.
        raise FeeTooLowException(
            message=f'Fee size too small per network policy. Recommended fee size: {recommended_fee}',
            fee=recommended_fee)
