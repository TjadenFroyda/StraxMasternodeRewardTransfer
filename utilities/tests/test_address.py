import pytest
from utilities import Network, Address
from .generators import random_string_generator


def test_create_valid_address():
    strax_addr = 'X' + random_string_generator(33)
    assert Address(address=strax_addr, network=Network.STRAX) == strax_addr

    strax_federation_addr = 'y' + random_string_generator(33)
    assert Address(address=strax_federation_addr, network=Network.STRAX) == strax_federation_addr

    cirrus_addr = 'C' + random_string_generator(33)
    assert Address(address=cirrus_addr, network=Network.CIRRUS) == cirrus_addr

    cirrus_federation_addr = 'c' + random_string_generator(33)
    assert Address(address=cirrus_federation_addr, network=Network.CIRRUS) == cirrus_federation_addr


def test_create_invalid_first_character():
    strax_addr = 'x' + random_string_generator(33)
    with pytest.raises(ValueError):
        Address(address=strax_addr, network=Network.STRAX)

    strax_federation_addr = 'Y' + random_string_generator(33)
    with pytest.raises(ValueError):
        Address(address=strax_federation_addr, network=Network.STRAX)

    cirrus_addr = 'd' + random_string_generator(33)
    with pytest.raises(ValueError):
        Address(address=cirrus_addr, network=Network.CIRRUS)


def test_create_address_too_long():
    strax_addr = 'X' + random_string_generator(36)
    with pytest.raises(ValueError):
        Address(address=strax_addr, network=Network.STRAX)

    strax_federation_addr = 'y' + random_string_generator(36)
    with pytest.raises(ValueError):
        Address(address=strax_federation_addr, network=Network.STRAX)

    cirrus_addr = 'C' + random_string_generator(36)
    with pytest.raises(ValueError):
        Address(address=cirrus_addr, network=Network.CIRRUS)

    cirrus_federation_addr = 'c' + random_string_generator(36)
    with pytest.raises(ValueError):
        Address(address=cirrus_federation_addr, network=Network.CIRRUS)


def test_create_address_too_short():
    strax_addr = 'X' + random_string_generator(30)
    with pytest.raises(ValueError):
        Address(address=strax_addr, network=Network.STRAX)

    strax_federation_addr = 'y' + random_string_generator(30)
    with pytest.raises(ValueError):
        Address(address=strax_federation_addr, network=Network.STRAX)

    cirrus_addr = 'C' + random_string_generator(30)
    with pytest.raises(ValueError):
        Address(address=cirrus_addr, network=Network.CIRRUS)

    cirrus_federation_addr = 'c' + random_string_generator(30)
    with pytest.raises(ValueError):
        Address(address=cirrus_federation_addr, network=Network.CIRRUS)


def test_create_address_invalid_characters():
    strax_addr = 'X' + random_string_generator(33)
    strax_addr = strax_addr[:16] + '[' + strax_addr[17:]
    with pytest.raises(ValueError):
        Address(address=strax_addr, network=Network.STRAX)

    strax_federation_addr = 'y' + random_string_generator(33)
    strax_federation_addr = strax_federation_addr[:16] + '[' + strax_federation_addr[17:]
    with pytest.raises(ValueError):
        Address(address=strax_federation_addr, network=Network.STRAX)

    cirrus_addr = 'C' + random_string_generator(33)
    cirrus_addr = cirrus_addr[:16] + '[' + cirrus_addr[17:]
    with pytest.raises(ValueError):
        Address(address=cirrus_addr, network=Network.CIRRUS)

    cirrus_federation_addr = 'c' + random_string_generator(33)
    cirrus_federation_addr = cirrus_federation_addr[:16] + '[' + cirrus_federation_addr[17:]
    with pytest.raises(ValueError):
        Address(address=cirrus_federation_addr, network=Network.CIRRUS)
