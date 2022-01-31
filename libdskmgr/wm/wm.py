from typing import List

from libdskmgr.common import Location

class WindowManager:
    def get_desktop_name(self, location: Location) -> str:
        raise NotImplementedError

    def create_desktop(self, location: Location) -> None:
        raise NotImplementedError

    def focus_desktop(self, location: Location) -> None:
        raise NotImplementedError

    def initialize_desktops(self, locations: List[Location]) -> None:
        raise NotImplementedError

    def remove_desktop(self, location: Location) -> None:
        raise NotImplementedError

    def change_desktop_location(self, old: Location, new: Location) -> None:
        raise NotImplementedError
