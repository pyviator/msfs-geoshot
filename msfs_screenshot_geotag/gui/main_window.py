from pathlib import Path
from typing import Optional

from msfs_screenshot_geotag.exif import ExifData, ExifService
from msfs_screenshot_geotag.sim import SimService, SimServiceError
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QCloseEvent, QDesktopServices, QKeySequence
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from .forms.main_window import Ui_MainWindow
from .notification import NotificationColor, NotificationHandler
from .screenshots import ImageFormat, ScreenshotService
from .settings import AppSettings
from .keyedit import CustomKeySequenceEdit

from .. import __app_name__

mock_exif_data = ExifData(
    GPSLatitude=60,
    GPSLongitude=60,
    GPSAltitude=100,
    GPSSpeed=200,  # m/s to km/h
)

class MainWindow(QMainWindow):

    closed = pyqtSignal()

    _maps_url = "https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"

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

        self._last_screenshot: Optional[Path] = None
        self._last_exif_data: Optional[ExifData] = None

        self._notification_handler = NotificationHandler(parent=self)

        self._form = Ui_MainWindow()
        self._form.setupUi(self)

        self._select_hotkey = CustomKeySequenceEdit(parent=self)
        self._form.layout_select_hotkey.addWidget(self._select_hotkey)

        self._load_ui_state_from_settings()

        self._setup_input_widget_connections()
        self._setup_button_connections()

        self.setWindowTitle(__app_name__)

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

        self._set_last_opened_screenshot(path=screenshot, exif_data=exif_data)

        return True

    def _setup_button_connections(self):
        self._form.select_folder.clicked.connect(self._on_select_folder)
        self._form.restore_defaults.clicked.connect(self._on_restore_defaults)
        self._form.open_screenshots.clicked.connect(self._on_open_folder)
        self._form.view_last_screenshot.clicked.connect(self._on_open_last_screenshot)
        self._form.view_last_location.clicked.connect(self._on_open_last_location)

    def _setup_input_widget_connections(self):
        self._form.select_format.currentTextChanged.connect(
            self._on_format_selection_changed
        )
        self._select_hotkey.keySequenceChanged.connect(self._on_hotkey_changed)

    def _tear_down_input_widget_connections(self):
        self._form.select_format.currentTextChanged.disconnect(
            self._on_format_selection_changed
        )
        self._select_hotkey.keySequenceChanged.disconnect(self._on_hotkey_changed)

    def _load_ui_state_from_settings(self):
        self._form.current_folder.setText(str(self._settings.screenshot_folder))
        self._select_hotkey.setKeySequence(
            QKeySequence(self._settings.screenshot_hotkey)
        )
        self._form.select_format.clear()
        self._form.select_format.addItems(format.name for format in ImageFormat)
        self._form.select_format.setCurrentText(self._settings.image_format.name)

    @pyqtSlot(bool)
    def _on_restore_defaults(self, checked: bool):
        self._settings.restore_defaults()
        # Avoid loops by temporarily disenganging connections
        self._tear_down_input_widget_connections()
        self._load_ui_state_from_settings()
        self._setup_input_widget_connections()

    @pyqtSlot(bool)
    def _on_select_folder(self, checked: bool):
        screenshot_folder = QFileDialog.getExistingDirectory(
            self,
            "Choose where to save MSFS screenshots",
            str(self._settings.screenshot_folder),
        )
        if not screenshot_folder:
            return

        self._form.current_folder.setText(screenshot_folder)
        self._settings.screenshot_folder = Path(screenshot_folder)

    @pyqtSlot(str)
    def _on_format_selection_changed(self, new_name: str):
        format = ImageFormat[new_name]
        self._settings.image_format = format

    @pyqtSlot(QKeySequence)
    def _on_hotkey_changed(self, new_hotkey: QKeySequence):
        if not new_hotkey or not new_hotkey.toString():
            return

        self._settings.screenshot_hotkey = new_hotkey.toString()

    @pyqtSlot(bool)
    def _on_open_folder(self, checked: bool):
        url = QUrl.fromLocalFile(str(self._settings.screenshot_folder))
        QDesktopServices.openUrl(url)

    def _set_last_opened_screenshot(
        self, path: Path, exif_data: Optional[ExifData] = None
    ):
        self._form.view_last_screenshot.setEnabled(True)
        self._last_screenshot = path

        if (
            exif_data
            and exif_data.GPSLatitude is not None
            and exif_data.GPSLongitude is not None
        ):
            self._form.view_last_location.setEnabled(True)
        self._last_exif_data = exif_data

    @pyqtSlot(bool)
    def _on_open_last_screenshot(self, checked: bool):
        if not self._last_screenshot:
            return
        url = QUrl.fromLocalFile(str(self._last_screenshot))
        QDesktopServices.openUrl(url)

    @pyqtSlot(bool)
    def _on_open_last_location(self, checked: bool):
        if not self._last_exif_data:
            return
        latitude = self._last_exif_data.GPSLatitude
        longitude = self._last_exif_data.GPSLongitude

        if latitude is None or longitude is None:
            print("Invalid GPS data for last screenshot")
            return

        url_str = self._maps_url.format(latitude=latitude, longitude=longitude)
        url = QUrl(url_str)
        QDesktopServices.openUrl(url)

    def closeEvent(self, close_event: QCloseEvent) -> None:
        self.closed.emit()
        return super().closeEvent(close_event)
