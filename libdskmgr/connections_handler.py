from socket import socket
from typing import List, Callable

from libdskmgr.common import Direction
from libdskmgr.desktop_manager import DesktopManager

class DskmgrConnectionsHandler:
    def __init__(self, desktop_manager: DesktopManager, max_recv_size = 4096) -> None:
        self._desktop_manager = desktop_manager
        self._max_recv_size = max_recv_size

    def _handle_new_x(self, args: List[str], connection: socket) -> None:
        self._desktop_manager.create_horizontal()
    
    def _handle_new_y(self, args: List[str], connection: socket) -> None:
        if len(args) == 1:
            group = self._desktop_manager.get_focused_group()
        elif len(args) == 2 and args[1].isnumeric():
            group = int(args[1])
        else:
            connection.sendall('Invalid arguments\n'.encode())
            return
        self._desktop_manager.create_vertical(group)

    def _handle_dump(self, args: List[str], connection: socket) -> None:
        connection.sendall(self._desktop_manager.dump_state().encode())

    def _handle_help(self, args: List[str], connection: socket) -> None:
        connection.sendall('TODO - usage\n'.encode())

    def _handle_move(self, args: List[str], connection: socket) -> None:
        DIRECTIONS = {
            'up':    Direction.UP,
            'down':  Direction.DOWN,
            'left':  Direction.LEFT,
            'right': Direction.RIGHT,
        }
        if len(args) != 2 or args[1] not in DIRECTIONS:
            connection.sendall('Invalid arguments\n'.encode())
        else:
            self._desktop_manager.move(DIRECTIONS[args[1]])

    def _handle_reset(self, args: List[str], connection: socket) -> None:
        if len(args) == 2 and args[1].isnumeric():
            self._desktop_manager.reset_desktops(int(args[1]))
        else:
            connection.sendall('Invalid arguments\n'.encode())
        
    def _handle_focus_group(self, args: List[str], connection: socket) -> None:
        if len(args) == 2 and args[1].isnumeric():
            self._desktop_manager.focus_group(int(args[1]))
        else:
            connection.sendall('Invalid arguments\n'.encode())

    def _get_handler(self, args: List[str]) -> Callable[[List[str], socket], None]:
        return self._handle_help if len(args) == 0 else {
            'reset': self._handle_reset,
            'new-x': self._handle_new_x,
            'new-y': self._handle_new_y,
            'dump': self._handle_dump,
            'move': self._handle_move,
            'goto': self._handle_focus_group,
        }.get(args[0]) or self._handle_help

    def handle_connection(self, connection: socket) -> None:
        data = connection.recv(self._max_recv_size)
        print('Recieved:', data)
        args = [arg.decode() for arg in data.split(b'\0') if arg]
        print('Args:', args)
        self._get_handler(args)(args, connection)
