from msfs_screenshot_geotag.gui.controller import ScreenShotController
import sys
from typing import List

from PyQt5.QtCore import QAbstractEventDispatcher
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QStyle
from pyqtkeybind import keybinder

from . import RESOURCES_PATH, __app_name__, __version__
from .exif import ExifService
from .gui.hotkeys import GlobalHotkeyService, Hotkey, WindowsEventFilter
from .gui.main_window import MainWindow
from .gui.settings import AppSettings
from .gui.tray_icon import AppTrayIcon
from .names import FileNameComposer
from .screenshots import ScreenshotService
from .sim import SimService


class Application(QApplication):
    def __init__(self, argv: List[str], name: str, version: str):
        super().__init__(argv)
        self.setApplicationName(name)
        self.setApplicationVersion(version)


def run():
    app = Application(argv=sys.argv, name=__app_name__, version=__version__)
    icon_window = QIcon(str(RESOURCES_PATH / "main.ico"))
    icon_tray = QIcon(str(RESOURCES_PATH / "tray.png"))
    app.setWindowIcon(icon_window)

    sim_service = SimService()
    exif_service = ExifService()
    file_name_composer = FileNameComposer()
    screenshot_service = ScreenshotService(file_name_composer)
    app_settings = AppSettings(app)

    screenshot_controller = ScreenShotController(
        sim_service=sim_service,
        exif_service=exif_service,
        screenshot_service=screenshot_service,
        file_name_composer=file_name_composer,
        settings=app_settings,
        parent=app,
    )

    main_window = MainWindow(
        file_name_composer=file_name_composer, settings=app_settings
    )

    screenshot_controller.sim_window_found.connect(main_window.on_sim_window_found)  # type: ignore
    screenshot_controller.screenshot_taken.connect(main_window.on_screenshot_taken)  # type: ignore
    screenshot_controller.error.connect(main_window.on_screenshot_error)  # type: ignore

    main_window.screenshot_requested.connect(screenshot_controller.take_screenshot)  # type: ignore

    tray_icon_widget = AppTrayIcon(icon_tray, main_window)
    main_window.closed.connect(tray_icon_widget.hide)

    keybinder.init()

    # For whatever reason, this only works when run in the context of this function:
    win_event_filter = WindowsEventFilter(keybinder)  # type: ignore
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    hotkey_service = GlobalHotkeyService(
        keybinder=keybinder, window_id=main_window.winId()  # type: ignore
    )
    hotkey_service.set_hotkeys(
        [
            Hotkey(
                key=app_settings.screenshot_hotkey,
                callback=screenshot_controller.take_screenshot,  # type: ignore
            )
        ]
    )

    main_window.closed.connect(hotkey_service.remove_hotkeys)

    tray_icon_widget.show()
    main_window.show()

    return app.exec()
