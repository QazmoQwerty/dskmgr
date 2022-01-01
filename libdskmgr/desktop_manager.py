import json
from typing import NamedTuple, List

from libdskmgr.wm.wm import WindowManager
from libdskmgr.common import Location, Direction
from libdskmgr.exceptions import GroupOutOfBoundsError, LocationOutOfBoundsError

class DesktopGroup:
    size: int
    current: int

    def __init__(self, size: int = 1, current: int = 0) -> None:
        self.size = size
        self.current = current

class DesktopManager:
    _groups: List[DesktopGroup]
    _focused_group: int
    _wm: WindowManager

    def __init__(self, wm: WindowManager) -> None:
        self._groups = [DesktopGroup()]
        self._focused_group = 0
        self._wm = wm
    
    def _is_in_bounds(self, loc: Location) -> bool:
        return 0 <= loc.x < len(self._groups) and 0 <= loc.y < self._groups[loc.x].size
    
    def _assert_group_in_bounds(self, group: int) -> None:
        if not self._is_in_bounds(Location(group, 0)):
            raise GroupOutOfBoundsError(group)
    
    def _assert_location_in_bounds(self, location, Location) -> None:
        if not self._is_in_bounds(location):
            raise LocationOutOfBoundsError(location)

    def reset_desktops(self, num_groups: int) -> None:
        locations = [Location(i, 0) for i in range(num_groups)]
        self._groups = [DesktopGroup() for i in range(num_groups)]
        self.focus_desktop(Location(0, 0))
        self._wm.initialize_desktops(locations)

    def get_focused_group(self) -> int:
        return self._focused_group

    def create_vertical(self, group: int) -> Location:
        self._assert_group_in_bounds(group)
        new_desktop_location = Location(group, self._groups[group].size)
        self._wm.create_desktop(new_desktop_location)
        self._groups[group].size += 1
        return new_desktop_location

    def create_horizontal(self) -> Location:
        new_desktop_location = Location(len(self._groups), 0)
        self._wm.create_desktop(new_desktop_location)
        self._groups += [DesktopGroup()]
        return new_desktop_location
    
    def focus_desktop(self, location: Location) -> None:
        self._assert_location_in_bounds(location)
        self._groups[location.x].current = location.y
        self._focused_group = location.x
        self._wm.focus_desktop(location)
    
    def focus_group(self, group: int) -> None:
        self._assert_group_in_bounds(group)
        self.focus_desktop(Location(group, self._groups[group].current))

    def dump_state(self) -> str:
        return json.dumps({
            'focused': self._focused_group,
            'groups': [{'size': group.size, 'y': group.current} for group in self._groups]
        })

    def move(self, direction: Direction) -> None:
        if direction in [Direction.UP, Direction.DOWN]: # move vertically
            vertical_offset = 1 if direction == Direction.UP else -1
            focused_group = self._groups[self._focused_group]
            new_y = (focused_group.current + vertical_offset) % focused_group.size
            self.focus_desktop(Location(self._focused_group, new_y))
        else: # move horizontally
            horizontal_offset = 1 if direction == Direction.RIGHT else -1
            new_x = (self._focused_group + horizontal_offset) % len(self._groups)
            self.focus_group(new_x)
