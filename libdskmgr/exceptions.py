from libdskmgr.common import Location

class DskmgrError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

from typing import Any

class LocationOutOfBoundsError(DskmgrError):
    def __init__(self, location: Location) -> None:
        super().__init__(f'Location {location.x}-{location.y} is out of bounds')

class GroupOutOfBoundsError(DskmgrError):
    def __init__(self, group: int) -> None:
        super().__init__(f'Group index {group} is out of bounds')
