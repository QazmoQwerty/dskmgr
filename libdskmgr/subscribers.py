from typing import Set

from libdskmgr.connection import Connection
from libdskmgr.desktop_manager import DesktopManager

class Subscribers:
    _desktop_manager: DesktopManager
    _subscriber_connections: Set[Connection]

    def __init__(self, desktop_manager: DesktopManager) -> None:
        self._desktop_manager = desktop_manager
        self._subscriber_connections = set()

    def add_subscriber(self, connection: Connection) -> None:
        self._subscriber_connections.add(connection)
        connection.set_auto_closeable(False)

    def update_all(self) -> None:
        state = self._desktop_manager.dump_state()
        closed_connections: Set[Connection] = set()
        for connection in self._subscriber_connections:
            try:
                connection.send(state)
            except:
                closed_connections.add(connection)

        for connection in closed_connections:
            self._subscriber_connections.remove(connection)
            connection.close()
