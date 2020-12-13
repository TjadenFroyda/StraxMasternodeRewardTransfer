from exceptions import RecommendedFeeTooHighException, EstimatePayloadException, BuildTransactionPayloadException
from typing import List, Union
from utilities import Money, Address, Network, Outpoint, Recipient


class TransactionPayload:
    """Creates a transaction payload to build and send on either STRAX or Cirrus network."""
    def __init__(self, network: Network):
        self._data = {}
        self._network = network
        self._amount = None

    @property
    def amount(self) -> Money:
        return Money(self._amount)

    @amount.setter
    def amount(self, val: Union[Money, int]) -> None:
        if not isinstance(val, Money) and not isinstance(val, int):
            raise ValueError('amount must be Money or int.')
        self._amount = Money(val)

    @property
    def sender(self) -> Address:
        return self._data.get('sender', None)

    @sender.setter
    def sender(self, val: Address) -> None:
        if not isinstance(val, Address):
            raise ValueError('sender must be an Address.')
        self._data['sender'] = Address(address=val, network=self._network)

    @property
    def fee_amount(self) -> Money:
        return self._data.get('feeAmount', Money(10000))

    @fee_amount.setter
    def fee_amount(self, val: Union[Money, int]) -> None:
        if not isinstance(val, int) and not isinstance(val, Money):
            raise ValueError('fee_amount must be Money or int.')

        # Validate and update recipient amount
        val = int(val)
        if val > 100000000:
            raise RecommendedFeeTooHighException(message='Setting fee higher than 1 CRS.', fee=Money(val))
        if val < 10000:
            print('Minimum fee is 10000. Adjusting.')
            val = 10000
        self._data['feeAmount'] = Money(val)
        if self.recipients is not None:
            self.recipients[0].amount = self.amount - Money(val)

    @property
    def password(self) -> str:
        return self._data.get('password', None)

    @password.setter
    def password(self, val: str) -> None:
        if not isinstance(val, str):
            raise ValueError('password must be a str.')
        self._data['password'] = val

    @property
    def segwit_change_address(self) -> bool:
        return self._data.get('segwitChangeAddress', False)

    @segwit_change_address.setter
    def segwit_change_address(self, val: bool) -> None:
        if not isinstance(val, bool):
            raise ValueError('segwit_change_address must be a bool.')
        self._data['segwitChangeAddress'] = val

    @property
    def wallet_name(self) -> str:
        return self._data.get('walletName', None)

    @wallet_name.setter
    def wallet_name(self, val: str) -> None:
        if not isinstance(val, str):
            raise ValueError('wallet_name must be a str.')
        self._data['walletName'] = val

    @property
    def account_name(self) -> str:
        return self._data.get('accountName', None)

    @account_name.setter
    def account_name(self, val: str) -> None:
        if not isinstance(val, str):
            raise ValueError('account_name must be a str.')
        self._data['accountName'] = val

    @property
    def outpoints(self) -> List[Outpoint]:
        return self._data.get('outpoints', None)

    @outpoints.setter
    def outpoints(self, val: List[Outpoint]) -> None:
        if not isinstance(val, list) and len(val) >= 1:
            raise ValueError('outpoints must be a list with length >= 1.')
        address = val[0].address
        outpoints = []
        for item in val:
            if not isinstance(item, Outpoint):
                raise ValueError('Each item must be an outpoint.')
            if address != item.address:
                raise ValueError('Each item must have the same address.')
            outpoints.append(item)
        self._data['outpoints'] = outpoints
        self.amount = sum([int(outpoint.amount) for outpoint in outpoints])
        self.sender = address

        # Updating the recipient amount
        if self.recipients is not None:
            self.recipients[0].amount = self.amount - self.fee_amount

    @property
    def recipients(self) -> List[Recipient]:
        return self._data.get('recipients', None)

    @recipients.setter
    def recipients(self, val: List[Recipient]) -> None:
        recipients = []
        if not isinstance(val, list) and len(val) == 1:
            raise ValueError('recipients must be a list with length == 1.')
        for item in val:
            if not isinstance(item, Recipient):
                raise ValueError('Each item must be a recipient.')
            recipients.append(item)

        if self.amount is not None:
            recipients[0].amount = self.amount - self.fee_amount
        self._data['recipients'] = recipients

    @property
    def allow_unconfirmed(self) -> bool:
        return self._data.get('allowUnconfirmed', True)

    @allow_unconfirmed.setter
    def allow_unconfirmed(self, val: bool) -> None:
        if not isinstance(val, bool):
            raise ValueError('allow_unconfirmed must be a bool.')
        self._data['allowUnconfirmed'] = val

    @property
    def shuffle_outputs(self) -> bool:
        return self._data.get('shuffleOutputs', False)

    @shuffle_outputs.setter
    def shuffle_outputs(self, val: bool) -> None:
        if not isinstance(val, bool):
            raise ValueError('shuffle_outputs must be a bool.')
        self._data['shuffleOutputs'] = val

    @property
    def change_address(self) -> Address:
        return self._data.get('changeAddress', None)

    @change_address.setter
    def change_address(self, val: Address) -> None:
        if not isinstance(val, Address):
            raise ValueError('change_address must be an Address.')
        self._data['changeAddress'] = Address(address=val, network=self._network)

    @property
    def opreturn_data(self) -> str:
        return self._data.get('opReturnData', None)

    @opreturn_data.setter
    def opreturn_data(self, val: str):
        self._data['opReturnData'] = str(val)

    def get_estimate_txfee_payload(self, crosschain: bool) -> dict:
        """Generates a payload dict specific for the estimate_txfee endpoint.

        :return: A txfee estimation payload.
        :rtype: dict
        :raises EstimatePayloadException: If required keys are not present.
        """
        required_keys = ['walletName', 'accountName', 'outpoints', 'recipients', 'feeType', 'changeAddress']
        estimate_txfee_payload_keys = ['walletName', 'accountName', 'outpoints', 'recipients', 'opReturnData',
                                       'opReturnAmount', 'feeType', 'allowUncofirmed', 'shuffleOutputs',
                                       'changeAddress']
        estimate_txfee_payload = {k: v for k, v in self._data.items() if k in estimate_txfee_payload_keys}

        # FeeType is specific to this endpoint.
        estimate_txfee_payload['feeType'] = 'low'

        if crosschain:
            required_keys.append('opReturnData')

        # Check to see if all the required keys are present.
        if not all(key in estimate_txfee_payload.keys() for key in required_keys):
            raise EstimatePayloadException(f'Not all required fields present. Required: {required_keys}.')

        return self._serialize_data(estimate_txfee_payload)

    def get_build_transaction_payload(self, crosschain: bool) -> dict:
        """Generates a payload dict specific for the build_transaction endpoint.

        :return: A build_transaction payload.
        :rtype: dict
        :raises BuildTransactionPayloadException: if required keys are not present.
        """
        required_keys = ['sender', 'walletName', 'accountName', 'password', 'outpoints', 'recipients', 'feeAmount', 'changeAddress']

        if crosschain:
            required_keys.append('opReturnData')

        if not all(key in self._data.keys() for key in required_keys):
            raise BuildTransactionPayloadException(f'Not all required fields present. Required: {required_keys}.')

        return self._serialize_data(self._data)

    def _serialize_data(self, data: dict) -> dict:
        """Serializes the payload"""
        payload = {}
        for k, v in data.items():
            if k in ['outpoints', 'recipients']:
                payload[k] = [item.serialize() for item in v]
            elif k in ['feeAmount', 'changeAddress', 'sender']:
                payload[k] = str(v)
            else:
                payload[k] = v
        return payload

    def __str__(self) -> str:
        return str(self._serialize_data(self._data))
