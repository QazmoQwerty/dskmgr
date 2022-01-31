import json
from typing import NamedTuple, List, Optional

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
    
    def _assert_location_in_bounds(self, location: Location) -> None:
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
    
    def focus_group(self, group: int) -> Location:
        self._assert_group_in_bounds(group)
        location = Location(group, self._groups[group].current)
        self.focus_desktop(location)
        return location

    def dump_state(self) -> str:
        return json.dumps({
            'focused': self._focused_group,
            'groups': [{'size': group.size, 'y': group.current} for group in self._groups]
        })

    def get_movement(self, direction: Direction) -> Location:
        if direction in [Direction.UP, Direction.DOWN]: # move vertically
            vertical_offset = 1 if direction == Direction.UP else -1
            focused_group = self._groups[self._focused_group]
            new_y = (focused_group.current + vertical_offset) % focused_group.size
            return Location(self._focused_group, new_y)
        else: # move horizontally
            horizontal_offset = 1 if direction == Direction.RIGHT else -1
            new_x = (self._focused_group + horizontal_offset) % len(self._groups)
            self._assert_group_in_bounds(new_x)
            return Location(new_x, self._groups[new_x].current)

    def move(self, direction: Direction) -> Location:
        location = self.get_movement(direction)
        self.focus_desktop(location)
        return location

    def get_desktop_name(self, location: Location) -> str:
        return self._wm.get_desktop_name(location)
    
    def _get_current_location(self) -> Location:
        return Location(self._focused_group, self._groups[self._focused_group].current)

    def remove(self, location: Optional[Location] = None) -> None:
        print('focused group:', self._focused_group)
        current = self._get_current_location()
        if location is None:
            location = current

        if len(self._groups) == 1 and self._groups[0].size == 1:
            return # Can't remove the last desktop!

        stay_in_place = False

        if current.x == location.x:
            if current.y == location.y:
                if self._groups[current.x].size == 1:
                    if current.x != 0:
                        self.move(Direction.LEFT)
                    else:
                        self.move(Direction.RIGHT)
                        self._focused_group = 0
                elif current.y != 0:
                    self.move(Direction.DOWN)
                else:
                    self.move(Direction.UP)
                    self._groups[current.x].current = 0
            elif current.y > location.y:
                self._groups[current.x].current -= 1
        elif current.x > location.x and self._groups[location.x].size == 1:
            self._focused_group -= 1

        self._wm.remove_desktop(location)
        for y in range(location.y + 1, self._groups[location.x].size):
            self._wm.change_desktop_location(Location(location.x, y), Location(location.x, y - 1))
        self._groups[location.x].size -= 1

        if self._groups[location.x].size == 0:
            for x in range(location.x + 1, len(self._groups)):
                for y in range(self._groups[x].size):
                    self._wm.change_desktop_location(Location(x, y), Location(x - 1, y))
            self._groups = self._groups[:location.x] + self._groups[location.x + 1:]
