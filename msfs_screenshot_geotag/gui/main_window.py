from typing import TYPE_CHECKING

from PyQt5.QtCore import QAbstractEventDispatcher, QAbstractNativeEventFilter
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from pyqtkeybind import keybinder

from .screenshots import ScreenShotService

if TYPE_CHECKING:
    from pyqtkeybind.win import WinKeyBinder


class WindowsEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder: "WinKeyBinder"):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


class MainWindow(QMainWindow):

    _hotkey = "Ctrl+Shift+S"

    def __init__(self, screenshot_service: ScreenShotService):
        super().__init__()

        self._screenshot_service = screenshot_service

        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget(self)
        self.central_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(self.central_layout)
        self.setCentralWidget(central_widget)
        self.central_layout.addWidget(QLabel("My label", parent=central_widget))
        self.central_layout.addWidget(QPushButton("My button", parent=central_widget))

    def _setup_global_keybinds(self):
        keybinder.init()
        keybinder.register_hotkey(
            self.winId(), self._hotkey, self._on_screenshot_hotkey
        )
        windows_event_filter = WindowsEventFilter(keybinder)  # type: ignore
        event_dispatcher = QAbstractEventDispatcher.instance()
        event_dispatcher.installNativeEventFilter(windows_event_filter)

    def _on_screenshot_hotkey(self):
        pass

    def closeEvent(self, close_event: QCloseEvent) -> None:
        try:
            keybinder.unregister_hotkey(self.winId(), self._hotkey)
        except Exception as e:
            print(e)
        return super().closeEvent(close_event)
