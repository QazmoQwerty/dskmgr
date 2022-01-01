from libdskmgr.server import UnixSocketServer
from libdskmgr.desktop_manager import DesktopManager
from libdskmgr.wm.wm_factory import WindowManagerFactory
from libdskmgr.connections_handler import DskmgrConnectionsHandler

def main() -> int:
    desktop_manager = DesktopManager(WindowManagerFactory().create('bspwm-mock'))
    connections_handler = DskmgrConnectionsHandler(desktop_manager)
    with UnixSocketServer('/tmp/dskmgr_socket', connections_handler.handle_connection) as server:
        server.run()
    return 1

if __name__ == '__main__':
    main()
