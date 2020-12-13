class NodeResponseException(Exception):
    def __init__(self, message: str, response: str):
        self.message = message
        self.response = response
        super().__init__(self.message)
