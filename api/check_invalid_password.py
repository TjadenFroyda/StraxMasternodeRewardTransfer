from exceptions import NodeResponseException
from .ErrorResponse import ErrorResponse


def check_invalid_password(error: ErrorResponse) -> None:
    for message in error.messages:
        if 'Invalid password (or invalid Network)' in message:
            raise NodeResponseException(message='Invalid password.', response=str(error.json))
