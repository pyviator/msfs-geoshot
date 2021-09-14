# MSFS Screenshot GeoTag

import sys
from pathlib import Path

from PyQt5.QtCore import QAbstractEventDispatcher, QAbstractNativeEventFilter
from pyqtkeybind import keybinder

from msfs_screenshot_geotag import __app_name__, __version__
from msfs_screenshot_geotag.exif import ExifService
from msfs_screenshot_geotag.gui.app import Application
from msfs_screenshot_geotag.gui.hotkeys import (
    GlobalHotkeyService,
    Hotkey,
    WindowsEventFilter,
)
from msfs_screenshot_geotag.gui.main_window import MainWindow
from msfs_screenshot_geotag.gui.screenshots import ScreenShotService
from msfs_screenshot_geotag.sim import SimService


def run():
    app = Application(argv=sys.argv, name=__app_name__, version=__version__)
    sim_service = SimService()
    exif_service = ExifService()
    screenshot_service = ScreenShotService(
        sim_service=sim_service, exif_service=exif_service, target_folder=Path.home()
    )
    main_window = MainWindow(screenshot_service=screenshot_service)

    keybinder.init()

    win_event_filter = WindowsEventFilter(keybinder)  # type: ignore
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    hotkey_service = GlobalHotkeyService(
        keybinder=keybinder, window_id=main_window.winId()  # type: ignore
    )

    with hotkey_service.hotkeys_set(
        hotkeys=[Hotkey(key="Ctrl+Shift+S", callback=main_window.take_screenshot)]
    ):
        main_window.show()
        ret = app.exec()

    return ret


sys.exit(run())
