import pytest
from utilities import Network, Money, Recipient
from .generators import generate_cirrus_address


def test_recipient_is_successful():
    cirrus_address = generate_cirrus_address()
    recipient = Recipient(network=Network.CIRRUS, item={'destinationAddress': cirrus_address})
    recipient.amount = 10000
    assert recipient.destination_address == cirrus_address
    assert isinstance(recipient.amount, Money)
    assert recipient.amount == 10000
    assert str(recipient.amount) == '0.00010000'
    assert str(recipient) == str({'destinationAddress': str(cirrus_address), 'amount': str(recipient.amount)})
    assert str(recipient.serialize()) == str({'destinationAddress': str(cirrus_address), 'amount': str(recipient.amount)})


def test_recipient_decimal_amount_raises_valueerror():
    recipient = Recipient(network=Network.CIRRUS, item={'destinationAddress': generate_cirrus_address()})
    with pytest.raises(TypeError):
        recipient.amount = 0.00001
