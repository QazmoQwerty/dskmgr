from typing import List, Set
import subprocess

from libdskmgr.common import Location
from libdskmgr.wm.wm import WindowManager

class Bspwm(WindowManager):
    _monitors: Set[str]

    def __init__(self) -> None:
        self._monitors = set(subprocess.check_output(['bspc', 'query', '--monitors', '--names']).decode().split())

    @staticmethod
    def _get_focused_monitor() -> str:
        return subprocess.check_output(['bspc', 'query', '--monitors', '-d', '--names']).decode().strip()

    @staticmethod
    def _get_desktop_name(location: Location, monitor_name: str) -> str:
        return f'{location.x}-{location.y}_{monitor_name}'

    @staticmethod
    def _focus_desktop(location: Location, monitor: str) -> None:
        subprocess.run(['bspc', 'desktop', '--focus', Bspwm._get_desktop_name(location, monitor)])

    def create_desktop(self, location: Location) -> None:
        for monitor in self._monitors:
            subprocess.run(['bspc', 'monitor', monitor, '--add-desktops', Bspwm._get_desktop_name(location, monitor)])

    def focus_desktop(self, location: Location) -> None:
        focused_monitor = Bspwm._get_focused_monitor()
        for monitor in self._monitors:
            if monitor != focused_monitor:
                Bspwm._focus_desktop(location, monitor)
        Bspwm._focus_desktop(location, focused_monitor)

    def initialize_desktops(self, locations: List[Location]) -> None:
        for monitor in self._monitors:
            subprocess.run(['bspc', 'monitor', '--reset-desktops', *[Bspwm._get_desktop_name(i, monitor) for i in locations]])
