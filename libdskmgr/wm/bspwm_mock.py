from typing import List

from libdskmgr.common import Location
from libdskmgr.wm.wm import WindowManager

class BspwmMock(WindowManager):
    @staticmethod
    def _get_desktop_name(location: Location) -> str:
        return f'{location.x}-{location.y}'

    def create_desktop(self, location: Location) -> None:
        print(f"Creating {BspwmMock._get_desktop_name(location)}")

    def focus_desktop(self, location: Location) -> None:
        print(f"Focusing {BspwmMock._get_desktop_name(location)}")

    def initialize_desktops(self, locations: List[Location]) -> None:
        print(f"Initializing desktops [{', '.join(map(BspwmMock._get_desktop_name, locations))}]")
