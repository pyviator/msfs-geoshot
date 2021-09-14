from typing import TYPE_CHECKING
from PyQt5.QtCore import pyqtSignal

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
from .notification import NotificationHandler


class MainWindow(QMainWindow):

    closed = pyqtSignal()

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

    def take_screenshot(self):
        screenshot = self._screenshot_service.take_screenshot()
        if screenshot:
            screenshot_name = screenshot.name
            message = f"<b>Screenshot saved</b>: {screenshot_name}"
            color = "#90ee90"
        else:
            message = "<b>Error</b>: Could not connect to Simulator"
            color = "#ffcccb"
        notification_handler = NotificationHandler(parent=self)
        notification_handler.notify(message=message, color=color)

    def closeEvent(self, close_event: QCloseEvent) -> None:
        self.closed.emit()
        return super().closeEvent(close_event)