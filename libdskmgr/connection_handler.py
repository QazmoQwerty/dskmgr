from socket import socket
from typing import List, Callable

from libdskmgr.common import Direction
from libdskmgr.connection import Connection
from libdskmgr.exceptions import DskmgrError
from libdskmgr.subscribers import Subscribers
from libdskmgr.desktop_manager import DesktopManager

class ConnectionHandler:
    def handle_connection(self, connection: Connection) -> None:
        raise NotImplementedError

class DskmgrConnectionHandler(ConnectionHandler):
    _desktop_manager: DesktopManager
    _subscribers: Subscribers

    def __init__(self, desktop_manager: DesktopManager) -> None:
        self._desktop_manager = desktop_manager
        self._subscribers = Subscribers(desktop_manager)

    def _handle_new_x(self, args: List[str], connection: Connection) -> None:
        self._desktop_manager.create_horizontal()
        self._subscribers.update_all()
    
    def _handle_new_y(self, args: List[str], connection: Connection) -> None:
        if len(args) == 1:
            group = self._desktop_manager.get_focused_group()
        elif len(args) == 2 and args[1].isnumeric():
            group = int(args[1])
        else:
            connection.send_error('Invalid arguments')
            return
        self._desktop_manager.create_vertical(group)
        self._subscribers.update_all()

    def _handle_dump(self, args: List[str], connection: Connection) -> None:
        connection.send(self._desktop_manager.dump_state())

    def _handle_no_arguments(self, args: List[str], connection: Connection) -> None:
        connection.send_error('No arguments given')

    def _handle_unknown_command(self, args: List[str], connection: Connection) -> None:
        connection.send_error(f'Unknown command: {repr(args[0])}')

    def _handle_move(self, args: List[str], connection: Connection) -> None:
        DIRECTIONS = {
            'up':    Direction.UP,
            'down':  Direction.DOWN,
            'left':  Direction.LEFT,
            'right': Direction.RIGHT,
        }
        if len(args) == 3 and args[1] in DIRECTIONS:
            if args[2] in ('-v', '--verbose'):
                location = self._desktop_manager.move(DIRECTIONS[args[1]])
                connection.send(self._desktop_manager.get_desktop_name(location))
                self._subscribers.update_all()
                return
            if args[2] in ('-t', '--test'):
                location = self._desktop_manager.get_movement(DIRECTIONS[args[1]])
                connection.send(self._desktop_manager.get_desktop_name(location))
                return
            return
        elif len(args) == 2 and args[1] in DIRECTIONS:
            self._desktop_manager.move(DIRECTIONS[args[1]])
            self._subscribers.update_all()
            return
        connection.send_error('Invalid arguments')

    def _handle_reset(self, args: List[str], connection: Connection) -> None:
        if len(args) == 2 and args[1].isnumeric():
            self._desktop_manager.reset_desktops(int(args[1]))
            self._subscribers.update_all()
        else:
            connection.send_error('Invalid arguments')

    def _handle_focus_group(self, args: List[str], connection: Connection) -> None:
        if len(args) == 2 and args[1].isnumeric():
            self._desktop_manager.focus_group(int(args[1]))
            self._subscribers.update_all()
        else:
            connection.send_error('Invalid arguments')

    def _handle_subscribe(self, args: List[str], connection: Connection) -> None:
        self._subscribers.add_subscriber(connection)

    def _get_handler(self, args: List[str]) -> Callable[[List[str], Connection], None]:
        return self._handle_no_arguments if len(args) == 0 else {
            'reset': self._handle_reset,
            'new-x': self._handle_new_x,
            'new-y': self._handle_new_y,
            'move': self._handle_move,
            'goto': self._handle_focus_group,
            'dump': self._handle_dump,
            'subscribe': self._handle_subscribe,
        }.get(args[0]) or self._handle_unknown_command

    def handle_connection(self, connection: Connection) -> None:
        args = connection.recv_args()
        print('Args:', args)
        try:
            self._get_handler(args)(args, connection)
        except DskmgrError as e:
            connection.send_error(str(e))
