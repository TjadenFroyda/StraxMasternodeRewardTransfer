import pytest
from utilities import Network, Money, Outpoint
from .generators import generate_transaction_hash, generate_strax_address, generate_cirrus_address


def test_outpoint_is_successful():
    transaction_hash = generate_transaction_hash()
    cirrus_address = generate_cirrus_address()

    outpoint = Outpoint(network=Network.CIRRUS, item={'address': cirrus_address, 'id': transaction_hash, 'index': 0, 'amount': Money(100)})

    assert outpoint.address == cirrus_address
    assert all(key in ('transactionId', 'index') for key in outpoint.serialize().keys())
    assert str(outpoint) == str({'transactionId': transaction_hash, 'index': 0})
    assert str(outpoint.serialize()) == str({'transactionId': transaction_hash, 'index': 0})


def test_output_network_mismatch():
    transaction_hash = generate_transaction_hash()

    with pytest.raises(ValueError):
        Outpoint(network=Network.STRAX, item={'address': generate_cirrus_address(), 'id': transaction_hash, 'index': 0, 'amount': Money(100)})
    with pytest.raises(ValueError):
        Outpoint(network=Network.CIRRUS, item={'address': generate_strax_address(), 'id': transaction_hash, 'index': 0, 'amount': Money(100)})


def test_outpoint_serialization_exception_missing_values():
    with pytest.raises(TypeError):
        outpoint = Outpoint(network=Network.CIRRUS, item={'address': generate_cirrus_address(), 'index': 0, 'amount': Money(100)})
        outpoint.serialize()
