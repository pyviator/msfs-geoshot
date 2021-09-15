from enum import Enum
from pathlib import Path
from typing import Optional

from PyQt5.QtCore import QObject, QSettings, QStandardPaths

from .. import __app_name__, __author__
from .screenshots import ImageFormat


class AppSettings(QObject):
    def __init__(self, parent: Optional[QObject]):
        super().__init__(parent)

        self._settings = QSettings(
            QSettings.Format.IniFormat,
            QSettings.Scope.UserScope,
            __author__,
            application=__app_name__,
            parent=self,
        )

    @property
    def screenshot_path(self) -> Path:
        raw_value = self._settings.value(
            "screenshot_path",
            defaultValue=QStandardPaths.writableLocation(
                QStandardPaths.PicturesLocation
            ),
        )

        return Path(raw_value)

    @screenshot_path.setter
    def screenshot_path(self, value: Path):
        self._settings.setValue("screenshot_path", str(value))

    @property
    def image_format(self) -> ImageFormat:
        raw_value = self._settings.value(
            "image_format", defaultValue=ImageFormat.tiff.name
        )
        return ImageFormat[raw_value]

    @image_format.setter
    def image_format(self, value: ImageFormat):
        self._settings.setValue("image_format", value.name)

    @property
    def screenshot_hotkey(self) -> str:
        return self._settings.value("screenshot_hotkey", defaultValue="Ctrl+Shift+S")

    @screenshot_hotkey.setter
    def screenshot_hotkey(self, value: str):
        self._settings.setValue("screenshot_hotkey", value)
