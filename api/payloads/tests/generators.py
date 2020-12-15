import string
from random import choice
from utilities import Address, Network


def generate_strax_address() -> Address:
    letters = string.ascii_letters + '0123456789'
    return Address(address='X' + ''.join(choice(letters) for _ in range(33)), network=Network.STRAX)


def generate_cirrus_address() -> Address:
    letters = string.ascii_letters + '0123456789'
    return Address(address='C' + ''.join(choice(letters) for _ in range(33)), network=Network.CIRRUS)


def generate_transaction_hash() -> str:
    letters = '0123456789abcdef'
    return ''.join(choice(letters) for _ in range(64))
