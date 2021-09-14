from msfs_screenshot_geotag.sim import SimService, SimServiceError
from typing import TYPE_CHECKING, Optional
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
from .notification import NotificationHandler, NotificationColor


class MainWindow(QMainWindow):

    closed = pyqtSignal()

    def __init__(self, sim_service: SimService, screenshot_service: ScreenShotService):
        super().__init__()

        self._sim_service = sim_service
        self._screenshot_service = screenshot_service
        self._notification_handler = NotificationHandler(parent=self)

        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget(self)
        self.central_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(self.central_layout)
        self.setCentralWidget(central_widget)
        self.central_layout.addWidget(QLabel("My label", parent=central_widget))
        self.central_layout.addWidget(QPushButton("My button", parent=central_widget))

    def take_screenshot(self) -> bool:
        try:
            location_data = self._sim_service.get_current_location()
        except SimServiceError as e:
            print(e)
            self._notification_handler.notify(
                message="<b>Error</b>: Could not connect to Simulator",
                color=NotificationColor.error,
            )
            return False

        screenshot = self._screenshot_service.take_screenshot(
            location_data=location_data
        )

        self._notification_handler.notify(
            message=f"<b>Screenshot saved</b>: {screenshot.name}",
            color=NotificationColor.success,
        )

        return True

    def closeEvent(self, close_event: QCloseEvent) -> None:
        self.closed.emit()
        return super().closeEvent(close_event)
