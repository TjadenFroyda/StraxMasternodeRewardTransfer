from api.payloads import TransactionPayload
from exceptions import BuildTransactionPayloadException, EstimatePayloadException
from random import choice
import string
import unittest
from utilities import Address, Network, Money, Outpoint, Recipient


class TransactionPayloadTests(unittest.TestCase):
    def setUp(self) -> None:
        self.strax_address = self._generate_strax_address()
        self.cirrus_address_sender = self._generate_cirrus_address()
        self.cirrus_address_recipient = self._generate_cirrus_address()
        self.transaction_ids = [self._generate_transaction_hash() for _ in range(7)]
        self.outpoints = [
            Outpoint(network=Network.CIRRUS, item={'address': self.cirrus_address_sender, 'id': self.transaction_ids[0], 'index': 0, 'amount': Money(200000)}),
            Outpoint(network=Network.CIRRUS, item={'address': self.cirrus_address_sender, 'id': self.transaction_ids[1], 'index': 0, 'amount': Money(200000)}),
            Outpoint(network=Network.CIRRUS, item={'address': self.cirrus_address_sender, 'id': self.transaction_ids[2], 'index': 0, 'amount': Money(200000)}),
            Outpoint(network=Network.CIRRUS, item={'address': self.cirrus_address_sender, 'id': self.transaction_ids[3], 'index': 0, 'amount': Money(200000)}),
            Outpoint(network=Network.CIRRUS, item={'address': self.cirrus_address_sender, 'id': self.transaction_ids[4], 'index': 0, 'amount': Money(200000)}),
            Outpoint(network=Network.CIRRUS, item={'address': self.cirrus_address_sender, 'id': self.transaction_ids[5], 'index': 0, 'amount': Money(200000)}),
            Outpoint(network=Network.CIRRUS, item={'address': self.cirrus_address_sender, 'id': self.transaction_ids[6], 'index': 0, 'amount': Money(200000)})
            ]
        self.amount = Money(sum([int(x.amount) for x in self.outpoints]))
        self.fee_amount = Money(10000)
        self.recipients = [Recipient(network=Network.CIRRUS, item={'destinationAddress': self.cirrus_address_recipient})]
        self.required_build_transaction_keys = ['walletName', 'accountName', 'password', 'outpoints', 'recipients', 'feeAmount', 'changeAddress', 'opReturnData']
        self.required_estimate_txfee_keys = ['walletName', 'accountName', 'outpoints', 'recipients', 'feeType', 'changeAddress', 'opReturnData']

    def tearDown(self) -> None:
        pass

    def _generate_strax_address(self) -> Address:
        letters = string.ascii_letters + '0123456789'
        return Address(address='X' + ''.join(choice(letters) for _ in range(33)), network=Network.STRAX)

    def _generate_cirrus_address(self) -> Address:
        letters = string.ascii_letters + '0123456789'
        return Address(address='C' + ''.join(choice(letters) for _ in range(33)), network=Network.CIRRUS)

    def _generate_transaction_hash(self) -> str:
        letters = '0123456789abcdef'
        return ''.join(choice(letters) for _ in range(64))

    def test_create_payload_is_successful(self):
        payload = TransactionPayload(network=Network.CIRRUS)
        payload.outpoints = self.outpoints
        payload.recipients = self.recipients
        payload.fee_amount = self.fee_amount
        payload.change_address = self.cirrus_address_sender
        payload.shuffle_outputs = False
        payload.allow_unconfirmed = True
        payload.segwit_change_address = False
        payload.opreturn_data = self.strax_address
        assert payload.amount == 1400000
        assert payload.fee_amount == 10000

    def test_create_payload_recipient_changed_fee_amount_updated(self):
        payload = TransactionPayload(network=Network.CIRRUS)
        payload.outpoints = self.outpoints
        payload.recipients = self.recipients
        payload.fee_amount = self.fee_amount
        new_recipients = [Recipient(network=Network.CIRRUS, item={'destinationAddress': self._generate_cirrus_address()})]
        payload.recipients = new_recipients
        assert payload.recipients[0].amount == self.amount - self.fee_amount
        assert payload.recipients[0].destination_address == new_recipients[0].destination_address

    def test_create_payload_get_estimate_txfee_payload_is_successful(self):
        payload = TransactionPayload(network=Network.CIRRUS)
        payload.wallet_name = 'test'
        payload.account_name = 'account 0'
        payload.outpoints = self.outpoints
        payload.recipients = self.recipients
        payload.fee_amount = self.fee_amount
        payload.change_address = self.cirrus_address_sender
        payload.shuffle_outputs = False
        payload.allow_unconfirmed = True
        payload.segwit_change_address = False
        payload.opreturn_data = self.strax_address

        estimate_txfee_payload = payload.get_estimate_txfee_payload(crosschain=True)

        assert all(key in estimate_txfee_payload.keys() for key in self.required_estimate_txfee_keys)
        assert isinstance(estimate_txfee_payload['outpoints'], list)
        assert len(estimate_txfee_payload['outpoints']) == len(self.outpoints)
        assert isinstance(estimate_txfee_payload['recipients'], list)
        assert len(estimate_txfee_payload['recipients']) == len(self.recipients)
        assert estimate_txfee_payload['recipients'][0]['destinationAddress'] == self.cirrus_address_recipient
        assert estimate_txfee_payload['recipients'][0]['amount'] == str(self.amount - self.fee_amount)
        assert estimate_txfee_payload['changeAddress'] == self.cirrus_address_sender
        assert estimate_txfee_payload['opReturnData'] == self.strax_address

    def test_create_payload_get_estimate_txfee_payload_missing_opreturn_on_crosschain_transfer_raises_exception(self):
        payload = TransactionPayload(network=Network.CIRRUS)
        payload.wallet_name = 'test'
        payload.account_name = 'account 0'
        payload.outpoints = self.outpoints
        payload.recipients = self.recipients
        payload.fee_amount = self.fee_amount
        payload.change_address = self.cirrus_address_sender
        payload.shuffle_outputs = False
        payload.allow_unconfirmed = True
        payload.segwit_change_address = False
        # payload.opreturn_data = self.strax_address

        with self.assertRaises(EstimatePayloadException):
            payload.get_estimate_txfee_payload(crosschain=True)

    def test_create_payload_get_estimate_txfee_payload_missing_recipients_raises_exception(self):
        payload = TransactionPayload(network=Network.CIRRUS)
        payload.wallet_name = 'test'
        payload.account_name = 'account 0'
        payload.outpoints = self.outpoints
        # payload.recipients = self.recipients
        payload.fee_amount = self.fee_amount
        payload.change_address = self.cirrus_address_sender
        payload.shuffle_outputs = False
        payload.allow_unconfirmed = True
        payload.segwit_change_address = False
        payload.opreturn_data = self.strax_address

        with self.assertRaises(EstimatePayloadException):
            payload.get_estimate_txfee_payload(crosschain=True)

    def test_create_payload_get_estimate_txfee_payload_missing_outpoints_raises_exception(self):
        payload = TransactionPayload(network=Network.CIRRUS)
        payload.wallet_name = 'test'
        payload.account_name = 'account 0'
        # payload.outpoints = self.outpoints
        with self.assertRaises(TypeError):
            payload.recipients = self.recipients
        payload.fee_amount = self.fee_amount
        payload.change_address = self.cirrus_address_sender
        payload.shuffle_outputs = False
        payload.allow_unconfirmed = True
        payload.segwit_change_address = False
        payload.opreturn_data = self.strax_address

        with self.assertRaises(EstimatePayloadException):
            payload.get_estimate_txfee_payload(crosschain=True)

    def test_create_payload_get_build_transaction_payload_is_successful(self):
        payload = TransactionPayload(network=Network.CIRRUS)
        payload.wallet_name = 'test'
        payload.account_name = 'account 0'
        payload.password = 'password'
        payload.outpoints = self.outpoints
        payload.recipients = self.recipients
        payload.fee_amount = self.fee_amount
        payload.change_address = self.cirrus_address_sender
        payload.shuffle_outputs = False
        payload.allow_unconfirmed = True
        payload.segwit_change_address = False
        payload.opreturn_data = self.strax_address

        build_transaction_payload = payload.get_build_transaction_payload(crosschain=True)

        assert all(key in build_transaction_payload.keys() for key in self.required_build_transaction_keys)
        assert isinstance(build_transaction_payload['outpoints'], list)
        assert len(build_transaction_payload['outpoints']) == len(self.outpoints)
        assert isinstance(build_transaction_payload['recipients'], list)
        assert len(build_transaction_payload['recipients']) == len(self.recipients)
        assert build_transaction_payload['recipients'][0]['destinationAddress'] == self.cirrus_address_recipient
        assert build_transaction_payload['recipients'][0]['amount'] == str(self.amount - self.fee_amount)
        assert build_transaction_payload['changeAddress'] == self.cirrus_address_sender
        assert build_transaction_payload['opReturnData'] == self.strax_address
        assert build_transaction_payload['feeAmount'] == str(self.fee_amount)

    def test_create_payload_get_build_transaction_payload_missing_opreturn_on_crosschain_raises_exception(self):
        payload = TransactionPayload(network=Network.CIRRUS)
        payload.wallet_name = 'test'
        payload.account_name = 'account 0'
        payload.password = 'password'
        payload.outpoints = self.outpoints
        payload.recipients = self.recipients
        payload.fee_amount = self.fee_amount
        payload.change_address = self.cirrus_address_sender
        payload.shuffle_outputs = False
        payload.allow_unconfirmed = True
        payload.segwit_change_address = False
        # payload.opreturn_data = self.strax_address

        with self.assertRaises(BuildTransactionPayloadException):
            payload.get_build_transaction_payload(crosschain=True)

    def test_create_payload_get_build_transaction_payload_missing_outpoints_raises_exception(self):
        payload = TransactionPayload(network=Network.CIRRUS)
        payload.wallet_name = 'test'
        payload.account_name = 'account 0'
        payload.password = 'password'
        # payload.outpoints = self.outpoints
        with self.assertRaises(TypeError):
            payload.recipients = self.recipients
        payload.fee_amount = self.fee_amount
        payload.change_address = self.cirrus_address_sender
        payload.shuffle_outputs = False
        payload.allow_unconfirmed = True
        payload.segwit_change_address = False
        payload.opreturn_data = self.strax_address

        with self.assertRaises(BuildTransactionPayloadException):
            payload.get_build_transaction_payload(crosschain=True)

    def test_create_payload_get_build_transaction_payload_missing_recipients_raises_exception(self):
        payload = TransactionPayload(network=Network.CIRRUS)
        payload.wallet_name = 'test'
        payload.account_name = 'account 0'
        payload.password = 'password'
        payload.outpoints = self.outpoints
        # payload.recipients = self.recipients
        payload.fee_amount = self.fee_amount
        payload.change_address = self.cirrus_address_sender
        payload.shuffle_outputs = False
        payload.allow_unconfirmed = True
        payload.segwit_change_address = False
        payload.opreturn_data = self.strax_address

        with self.assertRaises(BuildTransactionPayloadException):
            payload.get_build_transaction_payload(crosschain=True)


if __name__ == '__main__':
    unittest.main()
