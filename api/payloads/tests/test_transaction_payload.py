import pytest
from api.payloads import TransactionPayload
from exceptions import BuildTransactionPayloadException, EstimatePayloadException
from utilities import Network, Money, Outpoint, Recipient
from .generators import generate_transaction_hash, generate_cirrus_address, generate_strax_address


def test_create_payload_is_successful():
    num_outpoints = 7
    outpoint_amount = 20000
    fee_amount = 20000
    cirrus_address_sender = generate_cirrus_address()
    cirrus_address_recipient = generate_cirrus_address()
    outpoints = [
        Outpoint(
            network=Network.CIRRUS,
            item={'address': cirrus_address_sender, 'id': generate_transaction_hash(), 'index': 0, 'amount': Money(outpoint_amount)}) for _ in range(num_outpoints)
    ]
    payload = TransactionPayload(network=Network.CIRRUS)
    payload.outpoints = outpoints
    payload.recipients = [Recipient(network=Network.CIRRUS, item={'destinationAddress': cirrus_address_recipient})]
    payload.fee_amount = Money(fee_amount)
    payload.change_address = generate_cirrus_address()
    payload.shuffle_outputs = False
    payload.allow_unconfirmed = True
    payload.segwit_change_address = False
    payload.opreturn_data = generate_strax_address()

    assert payload.amount == outpoint_amount * num_outpoints
    assert payload.fee_amount == fee_amount


def test_create_payload_recipient_changed_fee_amount_updated():
    num_outpoints = 7
    outpoint_amount = 20000
    fee_amount = 20000
    cirrus_address_sender = generate_cirrus_address()
    cirrus_address_recipient = generate_cirrus_address()
    outpoints = [
        Outpoint(
            network=Network.CIRRUS,
            item={'address': cirrus_address_sender, 'id': generate_transaction_hash(), 'index': 0, 'amount': Money(outpoint_amount)}) for _ in range(num_outpoints)
    ]
    amount = Money(sum([int(x.amount) for x in outpoints]))
    payload = TransactionPayload(network=Network.CIRRUS)
    payload.outpoints = outpoints
    payload.recipients = [Recipient(network=Network.CIRRUS, item={'destinationAddress': cirrus_address_recipient})]
    payload.fee_amount = fee_amount
    new_recipients = [Recipient(network=Network.CIRRUS, item={'destinationAddress': generate_cirrus_address()})]
    payload.recipients = new_recipients

    assert payload.recipients[0].amount == amount - fee_amount
    assert payload.recipients[0].destination_address == new_recipients[0].destination_address


def test_create_payload_get_estimate_txfee_payload_is_successful():
    num_outpoints = 7
    outpoint_amount = 20000
    fee_amount = 20000
    cirrus_address_sender = generate_cirrus_address()
    cirrus_address_recipient = generate_cirrus_address()
    opreturn_address = generate_strax_address()
    outpoints = [
        Outpoint(
            network=Network.CIRRUS,
            item={'address': cirrus_address_sender, 'id': generate_transaction_hash(), 'index': 0, 'amount': Money(outpoint_amount)}) for _ in range(num_outpoints)
    ]
    amount = Money(sum([int(x.amount) for x in outpoints]))
    payload = TransactionPayload(network=Network.CIRRUS)
    payload.wallet_name = 'test'
    payload.account_name = 'account 0'
    payload.outpoints = outpoints
    payload.recipients = [Recipient(network=Network.CIRRUS, item={'destinationAddress': cirrus_address_recipient})]
    payload.fee_amount = fee_amount
    payload.change_address = cirrus_address_sender
    payload.shuffle_outputs = False
    payload.allow_unconfirmed = True
    payload.segwit_change_address = False
    payload.opreturn_data = opreturn_address

    estimate_txfee_payload = payload.get_estimate_txfee_payload(crosschain=True)

    assert all(key in estimate_txfee_payload.keys() for key in ['walletName', 'accountName', 'outpoints', 'recipients', 'feeType', 'changeAddress', 'opReturnData'])
    assert isinstance(estimate_txfee_payload['outpoints'], list)
    assert len(estimate_txfee_payload['outpoints']) == len(outpoints)
    assert isinstance(estimate_txfee_payload['recipients'], list)
    assert len(estimate_txfee_payload['recipients']) == len(payload.recipients)
    assert estimate_txfee_payload['recipients'][0]['destinationAddress'] == str(cirrus_address_recipient)
    assert estimate_txfee_payload['recipients'][0]['amount'] == str(amount - fee_amount)
    assert estimate_txfee_payload['changeAddress'] == str(cirrus_address_sender)
    assert estimate_txfee_payload['opReturnData'] == str(opreturn_address)


def test_create_payload_get_estimate_txfee_payload_missing_opreturn_on_crosschain_transfer_raises_exception():
    num_outpoints = 7
    outpoint_amount = 20000
    fee_amount = 20000
    cirrus_address_sender = generate_cirrus_address()
    cirrus_address_recipient = generate_cirrus_address()
    # opreturn_address = generate_strax_address()
    outpoints = [
        Outpoint(
            network=Network.CIRRUS,
            item={'address': cirrus_address_sender, 'id': generate_transaction_hash(), 'index': 0, 'amount': Money(outpoint_amount)}) for _ in range(num_outpoints)
    ]
    payload = TransactionPayload(network=Network.CIRRUS)
    payload.wallet_name = 'test'
    payload.account_name = 'account 0'
    payload.outpoints = outpoints
    payload.recipients = [Recipient(network=Network.CIRRUS, item={'destinationAddress': cirrus_address_recipient})]
    payload.fee_amount = fee_amount
    payload.change_address = cirrus_address_sender
    payload.shuffle_outputs = False
    payload.allow_unconfirmed = True
    payload.segwit_change_address = False
    # payload.opreturn_data = opreturn_address

    with pytest.raises(EstimatePayloadException):
        payload.get_estimate_txfee_payload(crosschain=True)


def test_create_payload_get_estimate_txfee_payload_missing_recipients_raises_exception():
    num_outpoints = 7
    outpoint_amount = 20000
    fee_amount = 20000
    cirrus_address_sender = generate_cirrus_address()
    # cirrus_address_recipient = generate_cirrus_address()
    outpoints = [
        Outpoint(
            network=Network.CIRRUS,
            item={'address': cirrus_address_sender, 'id': generate_transaction_hash(), 'index': 0, 'amount': Money(outpoint_amount)}) for _ in range(num_outpoints)
    ]
    payload = TransactionPayload(network=Network.CIRRUS)
    payload.wallet_name = 'test'
    payload.account_name = 'account 0'
    payload.outpoints = outpoints
    # payload.recipients = [Recipient(network=Network.CIRRUS, item={'destinationAddress': cirrus_address_recipient})]
    payload.fee_amount = fee_amount
    payload.change_address = cirrus_address_sender
    payload.shuffle_outputs = False
    payload.allow_unconfirmed = True
    payload.segwit_change_address = False
    payload.opreturn_data = generate_strax_address()

    with pytest.raises(EstimatePayloadException):
        payload.get_estimate_txfee_payload(crosschain=True)


def test_create_payload_get_estimate_txfee_payload_missing_outpoints_raises_exception():
    fee_amount = Money(20000)
    cirrus_address_recipient = generate_cirrus_address()
    payload = TransactionPayload(network=Network.CIRRUS)
    payload.wallet_name = 'test'
    payload.account_name = 'account 0'
    # payload.outpoints = self.outpoints
    with pytest.raises(TypeError):
        payload.recipients = [Recipient(network=Network.CIRRUS, item={'destinationAddress': cirrus_address_recipient})]
    payload.fee_amount = fee_amount
    payload.change_address = generate_cirrus_address()
    payload.shuffle_outputs = False
    payload.allow_unconfirmed = True
    payload.segwit_change_address = False
    payload.opreturn_data = generate_strax_address()

    with pytest.raises(EstimatePayloadException):
        payload.get_estimate_txfee_payload(crosschain=True)


def test_create_payload_get_build_transaction_payload_is_successful():
    num_outpoints = 7
    outpoint_amount = 20000
    fee_amount = 20000
    cirrus_address_sender = generate_cirrus_address()
    cirrus_address_recipient = generate_cirrus_address()
    opreturn_address = generate_strax_address()
    outpoints = [
        Outpoint(
            network=Network.CIRRUS,
            item={'address': cirrus_address_sender, 'id': generate_transaction_hash(), 'index': 0, 'amount': Money(outpoint_amount)}) for _ in range(num_outpoints)
    ]
    amount = Money(sum([int(x.amount) for x in outpoints]))
    payload = TransactionPayload(network=Network.CIRRUS)
    payload.wallet_name = 'test'
    payload.account_name = 'account 0'
    payload.password = 'password'
    payload.outpoints = outpoints
    payload.recipients = [Recipient(network=Network.CIRRUS, item={'destinationAddress': cirrus_address_recipient})]
    payload.fee_amount = fee_amount
    payload.change_address = cirrus_address_sender
    payload.shuffle_outputs = False
    payload.allow_unconfirmed = True
    payload.segwit_change_address = False
    payload.opreturn_data = opreturn_address

    build_transaction_payload = payload.get_build_transaction_payload(crosschain=True)

    assert all(key in build_transaction_payload.keys() for key in ['walletName', 'accountName', 'password', 'outpoints', 'recipients', 'feeAmount', 'changeAddress', 'opReturnData'])
    assert isinstance(build_transaction_payload['outpoints'], list)
    assert len(build_transaction_payload['outpoints']) == len(outpoints)
    assert isinstance(build_transaction_payload['recipients'], list)
    assert len(build_transaction_payload['recipients']) == len(payload.recipients)
    assert build_transaction_payload['recipients'][0]['destinationAddress'] == str(cirrus_address_recipient)
    assert build_transaction_payload['recipients'][0]['amount'] == str(amount - fee_amount)
    assert build_transaction_payload['changeAddress'] == str(cirrus_address_sender)
    assert build_transaction_payload['opReturnData'] == str(opreturn_address)
    assert build_transaction_payload['feeAmount'] == str(Money(fee_amount))


def test_create_payload_get_build_transaction_payload_missing_opreturn_on_crosschain_raises_exception():
    num_outpoints = 7
    outpoint_amount = 20000
    fee_amount = 20000
    cirrus_address_sender = generate_cirrus_address()
    cirrus_address_recipient = generate_cirrus_address()
    # opreturn_address = generate_strax_address()
    outpoints = [
        Outpoint(
            network=Network.CIRRUS,
            item={'address': cirrus_address_sender, 'id': generate_transaction_hash(), 'index': 0, 'amount': Money(outpoint_amount)}) for _ in range(num_outpoints)
    ]
    payload = TransactionPayload(network=Network.CIRRUS)
    payload.wallet_name = 'test'
    payload.account_name = 'account 0'
    payload.password = 'password'
    payload.outpoints = outpoints
    payload.recipients = [Recipient(network=Network.CIRRUS, item={'destinationAddress': cirrus_address_recipient})]
    payload.fee_amount = fee_amount
    payload.change_address = cirrus_address_sender
    payload.shuffle_outputs = False
    payload.allow_unconfirmed = True
    payload.segwit_change_address = False
    # payload.opreturn_data = opreturn_address

    with pytest.raises(BuildTransactionPayloadException):
        payload.get_build_transaction_payload(crosschain=True)


def test_create_payload_get_build_transaction_payload_missing_outpoints_raises_exception():
    fee_amount = Money(20000)
    cirrus_address_sender = generate_cirrus_address()
    cirrus_address_recipient = generate_cirrus_address()
    opreturn_address = generate_strax_address()
    payload = TransactionPayload(network=Network.CIRRUS)
    payload.wallet_name = 'test'
    payload.account_name = 'account 0'
    payload.password = 'password'
    # payload.outpoints = outpoints
    with pytest.raises(TypeError):
        payload.recipients = [Recipient(network=Network.CIRRUS, item={'destinationAddress': cirrus_address_recipient})]
    payload.fee_amount = fee_amount
    payload.change_address = cirrus_address_sender
    payload.shuffle_outputs = False
    payload.allow_unconfirmed = True
    payload.segwit_change_address = False
    payload.opreturn_data = opreturn_address

    with pytest.raises(BuildTransactionPayloadException):
        payload.get_build_transaction_payload(crosschain=True)


def test_create_payload_get_build_transaction_payload_missing_recipients_raises_exception():
    num_outpoints = 7
    outpoint_amount = 20000
    fee_amount = 20000
    cirrus_address_sender = generate_cirrus_address()
    # cirrus_recipient_address = generate_cirrus_address()
    opreturn_address = generate_strax_address()
    outpoints = [
        Outpoint(
            network=Network.CIRRUS,
            item={'address': cirrus_address_sender, 'id': generate_transaction_hash(), 'index': 0, 'amount': Money(outpoint_amount)}) for _ in range(num_outpoints)
    ]
    payload = TransactionPayload(network=Network.CIRRUS)
    payload.wallet_name = 'test'
    payload.account_name = 'account 0'
    payload.password = 'password'
    payload.outpoints = outpoints
    # payload.recipients = [Recipient(network=Network.CIRRUS, item={'destinationAddress': cirrus_address_recipient})]
    payload.fee_amount = fee_amount
    payload.change_address = cirrus_address_sender
    payload.shuffle_outputs = False
    payload.allow_unconfirmed = True
    payload.segwit_change_address = False
    payload.opreturn_data = opreturn_address

    with pytest.raises(BuildTransactionPayloadException):
        payload.get_build_transaction_payload(crosschain=True)
