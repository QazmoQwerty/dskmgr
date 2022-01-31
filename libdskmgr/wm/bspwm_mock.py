from typing import List

from libdskmgr.common import Location
from libdskmgr.wm.wm import WindowManager

class BspwmMock(WindowManager):
    DEFAULT_OUTPUT_FILE_PATH = '/tmp/dskmgr-bspwm_mock-output'

    _output_file_path: str

    def __init__(self, output_file_path: str = DEFAULT_OUTPUT_FILE_PATH) -> None:
        self._output_file_path = output_file_path

    def get_desktop_name(self, location: Location) -> str:
        return f'{location.x}-{location.y}'

    def _log(self, message: str) -> None:
        print(message)
        with open(self._output_file_path, 'a') as file:
            file.write(message + '\n')

    def create_desktop(self, location: Location) -> None:
        self._log(f"Creating {self.get_desktop_name(location)}")

    def focus_desktop(self, location: Location) -> None:
        self._log(f"Focusing {self.get_desktop_name(location)}")

    def initialize_desktops(self, locations: List[Location]) -> None:
        self._log(f"Initializing desktops [{', '.join(map(self.get_desktop_name, locations))}]")
