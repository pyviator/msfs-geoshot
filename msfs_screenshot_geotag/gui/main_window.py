import winsound
from pathlib import Path
from typing import Optional

from PyQt5.QtCore import QEvent, Qt, QTimer, QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QCloseEvent, QDesktopServices, QKeySequence
from PyQt5.QtWidgets import QApplication, QFileDialog, QLineEdit, QMainWindow

from .. import RESOURCES_PATH, __app_name__, __author__, __version__
from ..exif import ExifData
from ..names import FileNameComposer
from ..screenshots import ImageFormat
from .controller import ScreenShotResult
from .forms.main_window import Ui_MainWindow
from .keyedit import CustomKeySequenceEdit
from .notification import NotificationColor, NotificationHandler
from .settings import AppSettings
from .validators import DateFormatValidator, FileNameFormatValidator
from .hotkeys import HotkeyID

mock_exif_data = ExifData(
    GPSLatitude=30,
    GPSLongitude=30,
    GPSAltitude=100,
    GPSSpeed=200,  # m/s to km/h
)


class MainWindow(QMainWindow):

    screenshot_requested = pyqtSignal()
    hotkey_changed = pyqtSignal(HotkeyID, str)
    closed = pyqtSignal()

    _maps_url = "https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
    _shutter_sound_path = str(RESOURCES_PATH / "shutter.wav")

    def __init__(
        self,
        file_name_composer: FileNameComposer,
        settings: AppSettings,
    ):
        super().__init__()

        self._file_name_composer = file_name_composer
        self._settings = settings

        self._last_screenshot: Optional[Path] = None
        self._last_exif_data: Optional[ExifData] = None

        self._notification_handler = NotificationHandler(parent=self)

        self._form = Ui_MainWindow()
        self._form.setupUi(self)

        self._select_hotkey = CustomKeySequenceEdit(parent=self)
        self._form.layout_select_hotkey.addWidget(self._select_hotkey)
        self._form.open_screenshots.setFocus()  # prevent focus steal by hotkey

        self._load_ui_state_from_settings()
        self._setup_input_validators()
        self._setup_format_field_description()
        self._setup_button_labels()

        self._setup_input_widget_connections()
        self._setup_button_connections()

        self._form.title.setText(
            f"<b>{__app_name__}</b> v{__version__} by {__author__}"
        )
        self.setWindowTitle(__app_name__)

    @pyqtSlot(ScreenShotResult)
    def on_screenshot_taken(self, result: ScreenShotResult):
        self._notification_handler.notify(
            message=f"<b>Screenshot saved</b>: {result.path.name}",
            color=NotificationColor.success,
            onclick=self._on_open_last_screenshot,  # type: ignore
        )
        self._set_last_opened_screenshot(path=result.path, exif_data=result.exif_data)

    @pyqtSlot(str)
    def on_screenshot_error(self, message: str):
        self._notification_handler.notify(
            message=f"<b>Error</b>: {message}",
            color=NotificationColor.error,
        )

    @pyqtSlot()
    def on_sim_window_found(self):
        if self._settings.play_sound:
            winsound.PlaySound(
                self._shutter_sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC
            )

    def _setup_format_field_description(self):
        supported_fields = self._file_name_composer.get_supported_fields()

        lines = []

        for field in supported_fields:
            text = f"<b>{{{field.name}}}</b>: {field.description}"
            if field.required:
                text += " Required."
            lines.append(text)

        text = "<br>".join(lines)

        self._form.available_fields.setText(text)

    def _setup_input_validators(self):
        self._file_name_format_validator = FileNameFormatValidator(
            line_edit=self._form.file_name_format,
            warning_label=self._form.file_name_format_warning,
            save_button=self._form.file_name_format_save,
            file_name_composer=self._file_name_composer,
            parent=self,
        )
        self._date_format_validator = DateFormatValidator(
            line_edit=self._form.date_format,
            warning_label=self._form.date_format_warning,
            save_button=self._form.date_format_save,
            file_name_composer=self._file_name_composer,
            parent=self,
        )
        self._form.file_name_format.setValidator(self._file_name_format_validator)
        self._form.date_format.setValidator(self._date_format_validator)

    def _setup_button_connections(self):
        self._form.take_screenshot.clicked.connect(self.screenshot_requested)
        self._form.quit_button.clicked.connect(
            self._on_quit_button, Qt.ConnectionType.QueuedConnection
        )  # queued connection recommended on slots that close QApplication
        self._form.select_folder.clicked.connect(self._on_select_folder)
        self._form.restore_defaults.clicked.connect(self._on_restore_defaults)
        self._form.restore_defaults_advanced.clicked.connect(
            self._on_restore_defaults_advanced
        )
        self._form.open_screenshots.clicked.connect(self._on_open_folder)
        self._form.view_last_screenshot.clicked.connect(self._on_open_last_screenshot)
        self._form.view_last_location.clicked.connect(self._on_open_last_location)
        self._form.file_name_format_save.clicked.connect(self._on_file_name_format_save)
        self._form.date_format_save.clicked.connect(self._on_date_format_save)

    def _setup_button_labels(self):
        self._form.take_screenshot.setText(
            f"📷 Screenshot ({self._settings.screenshot_hotkey})"
        )

    def _setup_input_widget_connections(self):
        self._form.select_format.currentTextChanged.connect(
            self._on_format_selection_changed
        )
        self._select_hotkey.keySequenceChanged.connect(self._on_hotkey_changed)
        self._form.minimize_to_tray.stateChanged.connect(
            self._on_minimize_to_tray_changed
        )
        self._form.play_sound.stateChanged.connect(self._on_play_sound_changed)

    def _tear_down_input_widget_connections(self):
        self._form.select_format.currentTextChanged.disconnect(
            self._on_format_selection_changed
        )
        self._select_hotkey.keySequenceChanged.disconnect(self._on_hotkey_changed)
        self._form.minimize_to_tray.stateChanged.disconnect(
            self._on_minimize_to_tray_changed
        )
        self._form.play_sound.stateChanged.disconnect(self._on_play_sound_changed)

    def _load_ui_state_from_settings(self):
        self._form.current_folder.setText(str(self._settings.screenshot_folder))
        self._select_hotkey.setKeySequence(
            QKeySequence(self._settings.screenshot_hotkey)
        )
        self._form.select_format.clear()
        self._form.select_format.addItems(format.name for format in ImageFormat)
        self._form.select_format.setCurrentText(self._settings.image_format.name)
        self._form.file_name_format.setText(self._settings.file_name_format)
        self._form.date_format.setText(self._settings.date_format)
        self._form.minimize_to_tray.setChecked(self._settings.minimize_to_tray)
        self._form.play_sound.setChecked(self._settings.play_sound)

    @pyqtSlot()
    def _on_file_name_format_save(self):
        if not self._form.file_name_format.hasAcceptableInput():
            return  # should not happen
        self._settings.file_name_format = self._form.file_name_format.text()
        self._form.file_name_format.setPalette(QLineEdit().palette())
        self._form.file_name_format_save.setDisabled(True)

    @pyqtSlot()
    def _on_date_format_save(self):
        if not self._form.date_format.hasAcceptableInput():
            return  # should not happen
        self._settings.date_format = self._form.date_format.text()
        self._form.date_format.setPalette(QLineEdit().palette())
        self._form.date_format_save.setDisabled(True)

    @pyqtSlot()
    def _on_restore_defaults(self):
        self._settings.restore_defaults()
        # Avoid loops by temporarily disenganging connections
        self._tear_down_input_widget_connections()
        self._load_ui_state_from_settings()
        self._setup_input_widget_connections()
        self._setup_button_labels()
        # FIXME: should not have to do this manually
        self.hotkey_changed.emit(
            HotkeyID.take_screenshot, self._settings.defaults.screenshot_hotkey
        )

    @pyqtSlot()
    def _on_restore_defaults_advanced(self):
        self._form.file_name_format.setText(self._settings.defaults.file_name_format)
        self._form.date_format.setText(self._settings.defaults.date_format)
        self._form.file_name_format_save.click()
        self._form.date_format_save.click()

    @pyqtSlot()
    def _on_select_folder(self):
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

        key = new_hotkey.toString()
        self.hotkey_changed.emit(HotkeyID.take_screenshot, key)
        self._settings.screenshot_hotkey = key
        self._setup_button_labels()

    @pyqtSlot(int)
    def _on_minimize_to_tray_changed(self, state: int):
        self._settings.minimize_to_tray = state == Qt.CheckState.Checked

    @pyqtSlot(int)
    def _on_play_sound_changed(self, state: int):
        self._settings.play_sound = state == Qt.CheckState.Checked

    @pyqtSlot()
    def _on_open_folder(self):
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

    @pyqtSlot()
    def _on_open_last_screenshot(self):
        if not self._last_screenshot or not self._last_screenshot.is_file():
            self._notification_handler.notify(
                "File no longer exists", color=NotificationColor.error
            )
            return False
        url = QUrl.fromLocalFile(str(self._last_screenshot))
        QDesktopServices.openUrl(url)

    @pyqtSlot()
    def _on_open_last_location(self):
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

    @pyqtSlot()
    def _on_quit_button(self):
        self.closed.emit()
        QApplication.quit()

    def closeEvent(self, close_event: QCloseEvent) -> None:
        if self._settings.minimize_to_tray:
            self.showMinimized()
            close_event.ignore()
        else:
            self.closed.emit()
            return super().closeEvent(close_event)

    def changeEvent(self, event: QEvent):
        if event.type() != QEvent.Type.WindowStateChange:
            return super().changeEvent(event)
        if self.isMinimized() and self._settings.minimize_to_tray:
            event.ignore()
            QTimer.singleShot(0, self.hide)
