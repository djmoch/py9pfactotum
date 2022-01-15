import os
import socket
from .errors import FactotumSocketError


def server_socket() -> socket.socket:
    s = socket.socket(socket.AF_UNIX)
    if 'NAMESPACE' in os.environ:
        n = os.environ["NAMESPACE"]
        s.connect(f'{n}/factotum')
    elif 'USER' in os.environ and 'DISPLAY' in os.environ:
        u = os.environ['USER']
        d = os.environ['DISPLAY']
        s.connect(f'/tmp/ns.{u}.{d}/factotum')
    else:
        raise FactotumSocketError('cannot find factotum socket path')
    return s
