from cryptography.fernet import Fernet
import getpass


class Credentials:
    """A utility class for credential handling."""
    def __init__(self, wallet_name: str):
        self._encoding = 'utf-8'
        self._data = {}
        self.f = Fernet(Fernet.generate_key())
        self.wallet_name = wallet_name

    @property
    def f(self) -> Fernet:
        raise RuntimeWarning('f cannot be accessed.')

    @f.setter
    def f(self, val: Fernet) -> None:
        self._data['f'] = val

    @property
    def wallet_name(self) -> str:
        return self._data.get('wallet_name')

    @wallet_name.setter
    def wallet_name(self, val) -> None:
        if not isinstance(val, str):
            raise ValueError('wallet_name must be a string.')
        self._data['wallet_name'] = val

    @property
    def wallet_password(self) -> str:
        if self._data.get('wallet_password') is not None:
            return self._data['f'].decrypt(self._data.get('wallet_password')).decode(self._encoding)
        else:
            raise RuntimeWarning('Password is not yet set. Please run set_wallet_password.')

    @wallet_password.setter
    def wallet_password(self, val) -> None:
        if not isinstance(val, bytes):
            raise ValueError('wallet_password must be in bytes.')
        self._data['wallet_password'] = val

    def set_wallet_password(self) -> None:
        self.wallet_password = self._data['f'].encrypt(bytes(getpass.getpass('Password: '), self._encoding))
