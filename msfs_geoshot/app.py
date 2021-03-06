import sys
from typing import List

import multiexit
from PyQt5.QtCore import QAbstractEventDispatcher, QThreadPool
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QStyle
from pyqtkeybind import keybinder

from . import DEBUG, RESOURCES_PATH, __app_name__, __version__
from .gui.controller import ScreenShotController
from .gui.credits import show_credits
from .gui.error_handler import ErrorHandler, show_error
from .gui.feedback import FeedbackDialog
from .gui.hotkeys import GlobalHotkeyService, HotkeyID, WindowsEventFilter
from .gui.main_window import MainWindow
from .gui.settings import AppSettings
from .gui.thumbnails import ThumbnailMaker
from .gui.tray_icon import AppTrayIcon
from .metadata import MetadataService
from .names import FileNameComposer
from .screenshots import ScreenshotService
from .sim import SimService


class Application(QApplication):
    def __init__(self, argv: List[str], name: str, version: str):
        super().__init__(argv)
        self.setApplicationName(name)
        self.setApplicationVersion(version)


def run():
    multiexit.install(except_hook=False)
    app = Application(argv=sys.argv, name=__app_name__, version=__version__)

    if not DEBUG:
        error_handler = ErrorHandler(app)
        error_handler.exception_caught.connect(show_error)
        sys.excepthook = error_handler

    icon_window = QIcon(str(RESOURCES_PATH / "main.ico"))
    icon_tray = QIcon(str(RESOURCES_PATH / "tray.png"))
    app.setWindowIcon(icon_window)

    sim_service = SimService()
    metadata_service = MetadataService()
    file_name_composer = FileNameComposer()
    screenshot_service = ScreenshotService(file_name_composer)
    app_settings = AppSettings(app)

    screenshot_controller = ScreenShotController(
        sim_service=sim_service,
        metadata_service=metadata_service,
        screenshot_service=screenshot_service,
        file_name_composer=file_name_composer,
        settings=app_settings,
        parent=app,
    )

    main_window = MainWindow(
        file_name_composer=file_name_composer,
        settings=app_settings,
        app_icon=icon_window,
    )

    thumbnail_maker = ThumbnailMaker(
        thread_pool=QThreadPool.globalInstance(), thumbnail_height=96, parent=app
    )

    screenshot_controller.sim_window_found.connect(main_window.on_sim_window_found)  # type: ignore
    screenshot_controller.screenshot_taken.connect(main_window.on_screenshot_taken)  # type: ignore
    screenshot_controller.error.connect(main_window.on_screenshot_error)  # type: ignore

    screenshot_controller.screenshot_taken.connect(
        lambda result: thumbnail_maker.create_thumbnail(str(result.path))  # type: ignore
    )
    thumbnail_maker.thumb_ready.connect(main_window.on_thumbnail_ready)  # type: ignore

    main_window.screenshot_requested.connect(screenshot_controller.take_screenshot)  # type: ignore
    main_window.credits_requested.connect(lambda: show_credits(main_window))

    tray_icon_widget = AppTrayIcon(icon_tray, main_window)
    main_window.closed.connect(tray_icon_widget.hide)
    tray_icon_widget.quit_requested.connect(main_window.quit)  # type: ignore

    keybinder.init()

    # For whatever reason, this only works when run in the context of this function:
    win_event_filter = WindowsEventFilter(keybinder)  # type: ignore
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    hotkey_service = GlobalHotkeyService(keybinder=keybinder, parent=app)  # type: ignore

    # Hotkey not unbound will not be usable until system restart, so be extra careful:
    main_window.closed.connect(hotkey_service.unbind_all_hotkeys)

    def on_signal_exit():
        hotkey_service.unbind_all_hotkeys()
        tray_icon_widget.hide()
        app.exit()
        sys.exit(1)

    multiexit.register(on_signal_exit)

    hotkey_service.bind_hotkey(
        HotkeyID.take_screenshot, app_settings.screenshot_hotkey, main_window
    )
    hotkey_service.take_screenshot_pressed.connect(
        screenshot_controller.take_screenshot  # type: ignore
    )

    main_window.hotkey_changed.connect(
        lambda hotkey_id, key: hotkey_service.bind_hotkey(hotkey_id, key, main_window)
    )

    app_settings.times_launched += 1

    tray_icon_widget.show()
    if not app_settings.start_to_tray:
        main_window.show()

    if app_settings.times_launched == 10:
        feedback_dialog = FeedbackDialog(main_window)
        feedback_dialog.exec()

    return app.exec()
