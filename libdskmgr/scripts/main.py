from libdskmgr.server import UnixSocketServer
from libdskmgr.desktop_manager import DesktopManager
from libdskmgr.wm.wm_factory import WindowManagerFactory
from libdskmgr.connection_handler import DskmgrConnectionHandler

def main() -> int:
    desktop_manager = DesktopManager(WindowManagerFactory().create('bspwm-mock'))
    connection_handler = DskmgrConnectionHandler(desktop_manager)
    with UnixSocketServer('/tmp/dskmgr_socket', connection_handler) as server:
        server.run()
    return 1

if __name__ == '__main__':
    main()
