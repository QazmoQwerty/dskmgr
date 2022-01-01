import os
from typing import Callable
from socket import socket, AF_UNIX

class UnixSocketServer:
    def __init__(self, socket_path: str, connection_handler: Callable[[socket], None]) -> None:
        self._socket = socket(AF_UNIX)
        self._socket_path = socket_path
        self._connection_handler = connection_handler
        
    def __enter__(self) -> 'UnixSocketServer':
        self._socket.bind(self._socket_path)
        self._socket.listen()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self._socket.close()
        try:
            os.unlink(self._socket_path)
        except OSError:
            if os.path.exists(self._socket_path):
                print('Error: could not unlink socket file')

    def run(self) -> None:
        while True:
            connection, _ = self._socket.accept()
            with connection:
                self._connection_handler(connection)
