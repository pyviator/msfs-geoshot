from msfs_screenshot_geotag.exif import ExifData, ExifService
from msfs_screenshot_geotag.sim import SimService, SimServiceError
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget

from .notification import NotificationColor, NotificationHandler
from .screenshots import ScreenshotService
from .settings import AppSettings

mock_exif_data = ExifData(
    GPSLatitude=60,
    GPSLongitude=60,
    GPSAltitude=100,
    GPSSpeed=200,  # m/s to km/h
)


class MainWindow(QMainWindow):

    closed = pyqtSignal()

    def __init__(
        self,
        sim_service: SimService,
        exif_service: ExifService,
        screenshot_service: ScreenshotService,
        settings: AppSettings,
    ):
        super().__init__()

        self._sim_service = sim_service
        self._exif_service = exif_service
        self._screenshot_service = screenshot_service
        self._settings = settings

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
            exif_data = self._sim_service.get_flight_data()
        except SimServiceError as e:
            # print(e)
            # self._notification_handler.notify(
            #     message="<b>Error</b>: Could not connect to Simulator<br>or received invalid data",
            #     color=NotificationColor.error,
            # )
            exif_data = mock_exif_data  # DEBUG
            # return False

        screenshot = self._screenshot_service.take_screenshot(
            target_folder=self._settings.screenshot_folder,
            exif_data=exif_data,
            image_format=self._settings.image_format,
        )

        if exif_data:
            if not self._exif_service.write_data(
                image_path=screenshot, exif_data=exif_data
            ):
                self._notification_handler.notify(
                    message="<b>Error</b>: Could not write metadata to screenshot",
                    color=NotificationColor.error,
                )
                return False

        self._notification_handler.notify(
            message=f"<b>Screenshot saved</b>: {screenshot.name}",
            color=NotificationColor.success,
        )

        return True

    def closeEvent(self, close_event: QCloseEvent) -> None:
        self.closed.emit()
        return super().closeEvent(close_event)
