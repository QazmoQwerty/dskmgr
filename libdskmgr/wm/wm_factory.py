
from libdskmgr.wm.wm import WindowManager
from libdskmgr.wm.bspwm import Bspwm
from libdskmgr.wm.bspwm_mock import BspwmMock

class WindowManagerNotSupportedError(Exception):
    pass

class WindowManagerFactory:
    def create(self, wm_name: str) -> WindowManager:
        wm = {
            'bspwm': Bspwm,
            'bspwm-mock': BspwmMock,
        }.get(wm_name)
        if wm is None:
            raise WindowManagerNotSupportedError(f'Unsupported window manager {repr(wm_name)}')
        return wm()
