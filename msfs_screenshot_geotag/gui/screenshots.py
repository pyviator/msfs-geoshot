import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import tzlocal
from PyQt5.QtGui import QGuiApplication

from ..exif import ExifLocationData, ExifService
from ..sim import SimService, SimServiceError


class ScreenShotService:

    _date_format = "%Y-%m-%d-%H%M%S"
    _file_stem_format = "MSFS_{date}"
    _extension = "jpg"

    def __init__(
        self, sim_service: SimService, exif_service: ExifService, target_folder: Path
    ):
        self._sim_service = sim_service
        self._exif_service = exif_service
        self._target_folder = target_folder

    def take_screenshot(self) -> Optional[Path]:
        try:
            location_data = self._sim_service.get_current_location()
        except SimServiceError as e:
            print(e)
            return None

        out_path = self._get_new_screenshot_path()

        self._grab_screenshot(out_path)
        if location_data:
            self._write_metadata(location_data, out_path)

        return out_path

    def _get_new_screenshot_path(self) -> Path:
        capture_time = time.time()

        local_timezone = tzlocal.get_localzone()
        capture_datetime = datetime.fromtimestamp(capture_time, tz=local_timezone)
        datetime_string = capture_datetime.strftime(self._date_format)

        file_stem = self._file_stem_format.format(date=datetime_string)
        file_name = f"{file_stem}.{self._extension}"

        return self._target_folder / file_name

    def _grab_screenshot(self, out_path: Path):
        # TODO: identify actual window rather than using primary screen
        active_screen = QGuiApplication.primaryScreen()
        root_window = active_screen.grabWindow(0)  # type: ignore
        root_window.save(str(out_path), quality=100)

    def _write_metadata(self, location_data: ExifLocationData, screenshot: Path):
        self._exif_service.write_data(
            exif_location_data=location_data, image_path=screenshot
        )
