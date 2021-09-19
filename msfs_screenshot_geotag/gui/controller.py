from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

from msfs_screenshot_geotag.gui.settings import AppSettings
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from .. import MOCK_SIMULATOR
from ..exif import ExifData, ExifService
from ..names import FileNameComposer
from ..screenshots import ScreenshotService
from ..sim import SimService, SimServiceError
from ..windows import WindowRectangle, get_window_rectangle, raise_window_to_foreground


@dataclass
class ScreenShotResult:
    path: Path
    exif_data: Optional[ExifData]


_mock_exif_data = ExifData(
    GPSLatitude=30,
    GPSLongitude=30,
    GPSAltitude=100,
    GPSSpeed=200,
)


class ScreenShotController(QObject):

    sim_window_found = pyqtSignal()
    screenshot_taken = pyqtSignal(ScreenShotResult)
    error = pyqtSignal(str)

    def __init__(
        self,
        sim_service: SimService,
        exif_service: ExifService,
        screenshot_service: ScreenshotService,
        file_name_composer: FileNameComposer,
        settings: AppSettings,
        parent: Optional[QObject] = None,
    ):
        super().__init__(parent)
        self._sim_service = sim_service
        self._exif_service = exif_service
        self._screenshot_service = screenshot_service
        self._file_name_composer = file_name_composer
        self._settings = settings

    @pyqtSlot()
    def take_screenshot(self):
        screenshot_folder = self._settings.screenshot_folder
        if not screenshot_folder.is_dir():
            screenshot_folder.mkdir(parents=True, exist_ok=True)

        try:
            exif_data = self._sim_service.get_flight_data()
        except SimServiceError as e:
            if MOCK_SIMULATOR:
                exif_data = _mock_exif_data  # DEBUG
            else:
                print(e)
                self.error.emit(
                    "Could not connect to Simulator, or received invalid data"
                )
                return

        if MOCK_SIMULATOR:
            window_rectangle = WindowRectangle(0, 0, 1920, 1200)
        else:
            window_id = self._sim_service.get_simulator_main_window_id()
            raise_window_to_foreground(window_id)
            window_rectangle = get_window_rectangle(window_id)

        self.sim_window_found.emit()

        screenshot = self._screenshot_service.take_screenshot(
            window_rectangle=window_rectangle,
            target_folder=self._settings.screenshot_folder,
            file_name_format=self._settings.file_name_format,
            date_format=self._settings.date_format,
            exif_data=exif_data,
            image_format=self._settings.image_format,
        )

        if exif_data and not self._exif_service.write_data(
            image_path=screenshot, exif_data=exif_data
        ):
            self.error.emit("Could not write metadata to screenshot")
            return

        self.screenshot_taken.emit(
            ScreenShotResult(path=screenshot, exif_data=exif_data)
        )
