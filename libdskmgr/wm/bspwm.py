from typing import List
import subprocess

from libdskmgr.common import Location
from libdskmgr.wm.wm import WindowManager

class Bspwm(WindowManager):
    @staticmethod
    def _get_desktop_name(location: Location) -> str:
        return f'{location.x}-{location.y}'

    def create_desktop(self, location: Location) -> None:
        subprocess.run(['bspc', 'monitor', '--add-desktops', Bspwm._get_desktop_name(location)])

    def focus_desktop(self, location: Location) -> None:
        subprocess.run(['bspc', 'desktop', '--focus', Bspwm._get_desktop_name(location)])

    def initialize_desktops(self, locations: List[Location]) -> None:
        subprocess.run(['bspc', 'monitor', '--reset-desktops', *map(Bspwm._get_desktop_name, locations)])
