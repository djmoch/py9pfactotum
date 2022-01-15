"""
The factotum module implements a plan9port's auth(3) library.
"""
from typing import Dict
from .client import FactotumClient

__version__ = '0.1.0'


def auth_getuserpasswd(**kwargs: str) -> Dict[str, str]:
    """
    Retrieve a password from the factotum server. Kwargs should
    contain the desired key template. Returns a dictionary containing
    user and passwd keys.

    Proto and role may optionally be omitted from the key template;
    they are set within auth_getuserpasswd.
    """
    c = FactotumClient()
    return c.getpass(**kwargs)
