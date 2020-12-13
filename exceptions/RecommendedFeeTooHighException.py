from utilities import Money


class RecommendedFeeTooHighException(Exception):
    def __init__(self, message: str, fee: Money):
        self.message = message
        self.fee = fee
        super().__init__(self.message)
