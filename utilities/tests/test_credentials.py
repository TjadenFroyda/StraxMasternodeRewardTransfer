import unittest
import unittest.mock as mock
from utilities import Credentials


class CredentialsTests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_credentials_create_is_successful(self):
        creds = Credentials(wallet_name='test')
        assert creds.wallet_name == 'test'

    def test_credentials_set_password_is_successful(self):
        super_secret_password = 'd$fbm#@d30$%F@G4)5gf2^&}/'
        creds = Credentials(wallet_name='test')
        with mock.patch('getpass.getpass', return_value=super_secret_password):
            creds.set_wallet_password()

        # Decoded password is the same as original.
        assert creds.wallet_password == super_secret_password

        # Password kept in memory is encrypted.
        assert creds._data['wallet_password'] != super_secret_password


if __name__ == '__main__':
    unittest.main()
