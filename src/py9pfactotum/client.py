import enum

from contextlib import contextmanager
from typing import Any, Dict, Generator, Union
from ._vendor.py9p import py9p
from .errors import FactotumClientError
from .util import server_socket


@enum.unique
class _File(enum.Enum):
    CTL = 'ctl'
    RPC = 'rpc'
    PROTO = 'proto'
    CONFIRM = 'confirm'
    NEEDKEY = 'needkey'
    LOG = 'log'


@enum.unique
class Proto(enum.Enum):
    P9ANY = 'p9any'
    P9SK1 = 'p9sk1'
    P9SK2 = 'p9sk2'
    P9CR = 'p9cr'
    APOP = 'apop'
    CRAM = 'cram'
    CHAP = 'chap'
    DSA = 'dsa'
    MSCHAP = 'mschap'
    RSA = 'rsa'
    PASS = 'pass'
    VNC = 'vnc'
    WEP = 'wep'


@enum.unique
class Role(enum.Enum):
    CLIENT = 'client'
    SERVER = 'server'
    SPEAKSFOR = 'speaksfor'
    ENCRYPT = 'encrypt'
    DECRYPT = 'decrypt'
    SIGN = 'sign'
    VERIFY = 'verify'


class FactotumClient(py9p.Client):
    """Implements a Factotum 9p client"""

    def __init__(self) -> None:
        s = server_socket()
        c = py9p.Credentials('')
        super().__init__(s, c)

    @contextmanager
    def _connection(self, *args: Any,
                    **kwargs: Any) -> Generator[object, None, None]:
        try:
            self.open(*args, **kwargs)
            yield self
        finally:
            self.close()

    def _ctl(self, msg: Union[str, bytes]) -> None:
        if isinstance(msg, str):
            msg = bytes(msg, 'utf-8')
        with self._connection(_File.CTL.value):
            try:
                self.write(msg)
            except py9p.RpcError as r:
                raise FactotumClientError('_ctl', r)

    @staticmethod
    def _kwargs_to_key_tuple(**kwargs: str) -> str:
        """Converts a dictionary into a factotum key tuple."""
        s = ''
        for k, v in kwargs.items():
            if not isinstance(v, str):
                raise FactotumClientError(f'value of {k} is not a string', v)
            s = f'{s} {k}={v}'
        return s

    def debug(self) -> None:
        """Toggle debugging on the server"""
        self._ctl('debug')

    def getpass(self, **kwargs: str) -> Dict[str, str]:
        """Gets a password from the factotum server."""
        with self._connection(_File.RPC.value, py9p.ORDWR):
            try:
                if 'proto' in kwargs.keys() and kwargs['proto'] != 'pass':
                    raise FactotumClientError('getpass', 'wrong proto',
                                              kwargs['proto'])
                else:
                    kwargs['proto'] = 'pass'
                if 'role' in kwargs.keys() and kwargs['role'] != 'client':
                    raise FactotumClientError('getpass', 'wrong role',
                                              kwargs['role'])
                else:
                    kwargs['role'] = 'client'
                t = self._kwargs_to_key_tuple(**kwargs)
                self.write(bytes(f'start {t}', 'utf-8'))
                self.read(self.msize).decode('utf-8')
                self.write(b'read')
                r = self.read(self.msize).decode('utf-8').split(' ')
                if len(r) == 3:
                    user = r[1]
                    password = r[2]
                    r = r[0]
                else:
                    raise FactotumClientError(' '.join(r))
                if r != 'ok':
                    raise FactotumClientError(r)
                return {'user': user, 'passwd': password}
            except py9p.RpcError as r:
                raise FactotumClientError('getpass', r) from None

    def key(self, public: Dict[str, str], private: Dict[str, str]) -> None:
        """
        Add a key to the server via its control file. Public and
        private are dictionaries containing the keys and values.
        Keys in the private dictionary will be prepended with '!'
        before being sent to the server.
        """
        msg = 'key'
        for k, v in public.items():
            msg = f'{msg} {k}={v}'
        for k, v in public.items():
            msg = f'{msg} !{k}={v}'
        self._ctl(msg)

    def delkey(self, **kwargs: str) -> None:
        """Deletes a key from the factotum server."""
        msg = 'delkey'
        for k, v in kwargs.items():
            msg = f'{msg} {k}={v}'
        self._ctl(msg)
