from typing import List, Set, Optional
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

    def _focus_desktop(self, location: Location, monitor: str) -> None:
        subprocess.run(['bspc', 'desktop', '--focus', self.get_desktop_name(location, monitor)])

    def get_desktop_name(self, location: Location, monitor_name: Optional[str] = None) -> str:
        if monitor_name is None:
            return f'{location.x}-{location.y}'
        return f'{location.x}-{location.y}_{monitor_name}'

    def create_desktop(self, location: Location) -> None:
        for monitor in self._monitors:
            subprocess.run(['bspc', 'monitor', monitor, '--add-desktops', self.get_desktop_name(location, monitor)])

    def focus_desktop(self, location: Location) -> None:
        focused_monitor = Bspwm._get_focused_monitor()
        for monitor in self._monitors:
            if monitor != focused_monitor:
                self._focus_desktop(location, monitor)
        self._focus_desktop(location, focused_monitor)

    def initialize_desktops(self, locations: List[Location]) -> None:
        for monitor in self._monitors:
            subprocess.run(['bspc', 'monitor', '--reset-desktops', *[self.get_desktop_name(i, monitor) for i in locations]])

    def remove_desktop(self, location: Location) -> None:
        for monitor in self._monitors:
            subprocess.run(['bspc', 'desktop', self.get_desktop_name(location, monitor), '--remove'])
    
    def change_desktop_location(self, old: Location, new: Location) -> None:
        for monitor in self._monitors:
            subprocess.run(['bspc', 'desktop', self.get_desktop_name(old, monitor), '--rename', self.get_desktop_name(new, monitor)])
