from pytest_mock import MockerFixture
from utilities import Credentials


def test_credentials_create_is_successful():
    creds = Credentials(wallet_name='test')
    assert creds.wallet_name == 'test'


def test_credentials_set_password_is_successful(mocker: MockerFixture):
    super_secret_password = 'd$fbm#@d30$%F@G4)5gf2^&}/'
    creds = Credentials(wallet_name='test')
    mocker.patch('getpass.getpass', return_value=super_secret_password)
    creds.set_wallet_password()

    # Decoded password is the same as original.
    assert creds.wallet_password == super_secret_password

    # Password kept in memory is encrypted.
    assert creds._data['wallet_password'] != super_secret_password
