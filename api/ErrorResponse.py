from requests import Response


class ErrorResponse:
    def __init__(self, response: Response):
        self._json: dict = response.json()
        self._errors: list = self._json.get('errors', [])
        self._messages: list = [message.get('message', '') for message in self._errors]

    @property
    def json(self) -> dict:
        return self._json

    @property
    def errors(self) -> list:
        return self._errors

    @property
    def messages(self) -> list:
        return self._messages
