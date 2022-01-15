py9pfactotum
============

py9pfactotum is Python's plan9port Factotum client. It also provides
the following extras:

- Helper functions that mirror plan9port's auth(3) library
- A [Keyring](https://pypi.org/project/keyring/) backend to connect
  to your running factotum server.

Usage
-----

In the current (alpha) state of maturity, the implementation is
incomplete. Currently enough is implemented to support the Keyring
backend (i.e., to read passwords from the running server).

When using the FactotumClient directly, arguments are passed as
keyword arguments, which are built into a key template internally:

```
from py9pfactotum import FactotumClient
c = FactotumClient()
c.getpass(server='mail.example.org', user='johndoe')
{ 'user': 'johndoe', 'passwd': 'insecure' }
```

As with the example above, the client provides high-level methods
that supply the correct 'proto' and 'role' attributes to the key
template. See factotum(4) for more information.

When using the auth(3) functions, the function signatures mirror
their plan9port counterparts, except that structures are replaced
with dictionaries.

```
from py9pfactotum import auth_getuserpasswd
c = auth_getuserpasswd(server='mail.example.org')
{ 'user': 'johndoe', 'passwd': 'insecure' }
```

Keyring
-------

The Keyring user interface is transparent, but that library must
be explicitly installed on the system (it is not a hard dependency
of py9pfactotum). Because factotum is not able to persist passwords
(or password deletions), attempts to use the Keyring to do so will
throw an error.
