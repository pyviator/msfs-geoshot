from msfs_screenshot_geotag.names import FileNameComposer
import sys
from typing import List

from PyQt5.QtCore import QAbstractEventDispatcher
from PyQt5.QtWidgets import QApplication, QStyle
from pyqtkeybind import keybinder

from . import __app_name__, __version__
from .exif import ExifService
from .gui.hotkeys import GlobalHotkeyService, Hotkey, WindowsEventFilter
from .gui.main_window import MainWindow
from .gui.screenshots import ScreenshotService
from .gui.settings import AppSettings
from .gui.tray_icon import AppTrayIcon
from .sim import SimService


class Application(QApplication):
    def __init__(self, argv: List[str], name: str, version: str):
        super().__init__(argv)
        self.setApplicationName(name)
        self.setApplicationVersion(version)


def run():
    app = Application(argv=sys.argv, name=__app_name__, version=__version__)

    user_agent = __app_name__.replace(" ", "_")

    sim_service = SimService()
    exif_service = ExifService()
    file_name_composer = FileNameComposer(user_agent=user_agent)
    screenshot_service = ScreenshotService(file_name_composer=file_name_composer)
    app_settings = AppSettings(app)

    screenshot_folder = app_settings.screenshot_folder
    if not screenshot_folder.is_dir():
        screenshot_folder.mkdir(parents=True, exist_ok=True)

    main_window = MainWindow(
        sim_service=sim_service,
        exif_service=exif_service,
        screenshot_service=screenshot_service,
        settings=app_settings,
        file_name_composer=file_name_composer
    )

    pixmap = QStyle.StandardPixmap.SP_BrowserReload
    icon = app.style().standardIcon(pixmap)
    tray_icon = AppTrayIcon(icon, main_window)

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
                key=app_settings.screenshot_hotkey, callback=main_window.take_screenshot
            )
        ]
    )

    main_window.closed.connect(hotkey_service.remove_hotkeys)

    tray_icon.show()
    main_window.show()

    return app.exec()
