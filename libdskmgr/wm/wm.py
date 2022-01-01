from typing import List

from libdskmgr.common import Location

class WindowManager:
    def create_desktop(self, location: Location) -> None:
        raise NotImplementedError

    def focus_desktop(self, location: Location) -> None:
        raise NotImplementedError

    def initialize_desktops(self, locations: List[Location]) -> None:
        raise NotImplementedError
