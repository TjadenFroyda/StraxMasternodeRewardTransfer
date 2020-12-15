import re
from typing import Union
from utilities import Money
from .ErrorResponse import ErrorResponse


def try_extract_policy_minimum_from_error_message(error: ErrorResponse) -> Union[Money, None]:
    """Attempts to extract the policy minimum from the error message.

    :param ErrorResponse error: The error response.
    :return: The recommended fee, if found.
    :rtype: Union[Money, None]
    """
    recommended_fee = []
    r_policy = re.compile(r'The policy minimum is \b([0-9]\.[0-9]+)\b')
    # Try to extract the policy minimum recommended by the node's error message.
    for message in error.messages:
        # Should only match one message
        recommended_fee.extend([float(x) * 1e8 for x in r_policy.findall(message)])
    if len(recommended_fee) >= 1:
        return Money(int(max(recommended_fee)))
    return None
