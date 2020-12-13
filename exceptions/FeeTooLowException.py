from utilities import Money


class FeeTooLowException(Exception):
    def __init__(self, message: str, fee: Money):
        self.message = message
        self.recommended_fee = fee
        super().__init__(self.message)
