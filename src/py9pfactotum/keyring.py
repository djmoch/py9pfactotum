"""
The keyring module implements a keyring backend.
"""
from typing import NoReturn, Optional
from keyring.backend import KeyringBackend
from keyring.credentials import SimpleCredential
from keyring.errors import PasswordDeleteError, PasswordSetError
from keyring.util import properties
from .client import FactotumClient


class FactotumBackend(KeyringBackend):

    @properties.ClassProperty
    @classmethod
    def priority(cls):
        return 1

    def get_password(self, service: str, username: str) -> str:
        """Get password of the username for the service"""
        c = FactotumClient()
        r = c.getpass(server=service, user=username)
        return r['passwd']

    def set_password(self, service: str, username: str,
                     password: str) -> NoReturn:
        """
        We're not able to persist passwords through the factotum
        interface. The user should update the source file manually.
        """
        raise PasswordSetError("cannot update factotum file")

    def delete_password(self, service: str, username: str) -> NoReturn:
        """
        We're not able to delete passwords through the factotum
        interface. The user should update the source file manually.
        """
        raise PasswordDeleteError("cannot update factotum file")

    def get_credential(self, service: str,
                       username: Optional[str]) -> Optional[SimpleCredential]:
        """Gets the username and password for the service.
        Returns a Credential instance.
        The *username* argument is optional and may be omitted by
        the caller or ignored by the backend. Callers must use the
        returned username.
        """
        c = FactotumClient()
        if username:
            r = c.getpass(server=service, user=username)
        else:
            r = c.getpass(server=service)
        return SimpleCredential(r['user'], r['passwd'])
