from socket import socket
from typing import List, Callable

from libdskmgr.common import Direction
from libdskmgr.connection import Connection
from libdskmgr.exceptions import DskmgrError
from libdskmgr.desktop_manager import DesktopManager

class ConnectionHandler:
    def handle_connection(self, connection: Connection) -> None:
        raise NotImplementedError

class DskmgrConnectionHandler(ConnectionHandler):
    _desktop_manager: DesktopManager

    def __init__(self, desktop_manager: DesktopManager) -> None:
        self._desktop_manager = desktop_manager

    def _handle_new_x(self, args: List[str], connection: Connection) -> None:
        self._desktop_manager.create_horizontal()
    
    def _handle_new_y(self, args: List[str], connection: Connection) -> None:
        if len(args) == 1:
            group = self._desktop_manager.get_focused_group()
        elif len(args) == 2 and args[1].isnumeric():
            group = int(args[1])
        else:
            connection.send('Invalid arguments')
            return
        self._desktop_manager.create_vertical(group)

    def _handle_dump(self, args: List[str], connection: Connection) -> None:
        connection.send(self._desktop_manager.dump_state())

    def _handle_no_arguments(self, args: List[str], connection: Connection) -> None:
        connection.send('No arguments given')

    def _handle_unknown_command(self, args: List[str], connection: Connection) -> None:
        connection.send(f'Unknown command: {repr(arg[0])}')

    def _handle_move(self, args: List[str], connection: Connection) -> None:
        DIRECTIONS = {
            'up':    Direction.UP,
            'down':  Direction.DOWN,
            'left':  Direction.LEFT,
            'right': Direction.RIGHT,
        }
        if len(args) != 2 or args[1] not in DIRECTIONS:
            connection.send('Invalid arguments')
        else:
            self._desktop_manager.move(DIRECTIONS[args[1]])

    def _handle_reset(self, args: List[str], connection: Connection) -> None:
        if len(args) == 2 and args[1].isnumeric():
            self._desktop_manager.reset_desktops(int(args[1]))
        else:
            connection.send('Invalid arguments')
        
    def _handle_focus_group(self, args: List[str], connection: Connection) -> None:
        if len(args) == 2 and args[1].isnumeric():
            self._desktop_manager.focus_group(int(args[1]))
        else:
            connection.send('Invalid arguments')

    def _get_handler(self, args: List[str]) -> Callable[[List[str], Connection], None]:
        return self._handle_no_arguments if len(args) == 0 else {
            'reset': self._handle_reset,
            'new-x': self._handle_new_x,
            'new-y': self._handle_new_y,
            'dump': self._handle_dump,
            'move': self._handle_move,
            'goto': self._handle_focus_group,
        }.get(args[0]) or self._handle_unknown_command

    def handle_connection(self, connection: Connection) -> None:
        args = connection.recv_args()
        print('Args:', args)
        try:
            self._get_handler(args)(args, connection)
        except DskmgrError as e:
            # TODO - figure out how bspc expects errors to be shown
            connection.send(str(e))
