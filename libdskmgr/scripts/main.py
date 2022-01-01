import argparse
from typing import NamedTuple

from libdskmgr.version import VERSION
from libdskmgr.server import UnixSocketServer
from libdskmgr.desktop_manager import DesktopManager
from libdskmgr.wm.wm_factory import WindowManagerFactory
from libdskmgr.connection_handler import DskmgrConnectionHandler

class CmdArguments(NamedTuple):
    wm: str
    verbose: bool

def parse_arguments() -> CmdArguments:
    parser = argparse.ArgumentParser(description='Daemon process for dskmgr')
    parser.add_argument(
        '--wm',
        # dest='wm',
        type=str,
        default='bspwm',
        choices=('bspwm', 'bspwm-mock'),
        help='Set which window manager to control',
    )
    parser.add_argument('-V', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=VERSION,
    )
    args = parser.parse_args()
    return CmdArguments(args.wm, args.verbose)

def main() -> int:
    cmd_args = parse_arguments()
    wm_factory = WindowManagerFactory()
    desktop_manager = DesktopManager(wm_factory.create(cmd_args.wm))
    connection_handler = DskmgrConnectionHandler(desktop_manager)
    with UnixSocketServer('/tmp/dskmgr_socket', connection_handler) as server:
        server.run()
    return 1

if __name__ == '__main__':
    main()
