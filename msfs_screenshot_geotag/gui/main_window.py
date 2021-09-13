from typing import TYPE_CHECKING, Optional

from PyQt5.QtCore import QAbstractEventDispatcher, QAbstractNativeEventFilter
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from pyqtkeybind import keybinder

from .screenshots import ScreenShotService
from ..exif_service import ExifService
from ..sim_service import SimService

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

    def __init__(
        self,
        title: str,
        screenshot_service: ScreenShotService,
        parent: Optional[QWidget],
        **kwargs
    ):
        super().__init__(parent=parent, **kwargs)

        self._screenshot_service = screenshot_service

        self._setup_ui()

        self.setWindowTitle(title)

    def _setup_ui(self):
        central_widget = QWidget(self)
        self.central_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(self.central_layout)
        self.setCentralWidget(central_widget)
        self.central_layout.addWidget(QLabel("My label", parent=central_widget))
        self.central_layout.addWidget(QPushButton("My button", parent=central_widget))

    def _setup_global_keybinds(self):
        keybinder.init()
        keybinder.register_hotkey(self.wiId(), self._hotkey, self._on_screenshot_hotkey)

    def _on_screenshot_hotkey(self):
        pass
