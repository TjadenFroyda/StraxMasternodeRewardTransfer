import string
from random import choice
from utilities import Address, Network


def generate_transaction_hash() -> str:
    letters = '0123456789abcdef'
    return ''.join(choice(letters) for _ in range(64))


def generate_hexstring() -> str:
    letters = '0123456789abcdef'
    return ''.join(choice(letters) for _ in range(128))


def generate_cirrus_address() -> Address:
    letters = string.ascii_letters + '0123456789'
    return Address(address='C' + ''.join(choice(letters) for _ in range(33)), network=Network.CIRRUS)
