from enum import Enum
from pathlib import Path
from typing import Optional

from PyQt5.QtCore import QObject, QSettings, QStandardPaths

from .. import __app_name__, __author__
from .screenshots import ImageFormat

from dataclasses import dataclass, asdict


@dataclass
class _SettingsData:
    screenshot_folder: Path = (
        Path(QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)) / "MSFS"
    )
    image_format: ImageFormat = ImageFormat.TIFF
    screenshot_hotkey: str = "Ctrl+Shift+S"


class AppSettings(QObject):
    _defaults = _SettingsData()

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
    def screenshot_folder(self) -> Path:
        if (
            value := self._settings.value("screenshot_folder", defaultValue=None)
        ) is None:
            return self._defaults.screenshot_folder
        return Path(value)

    @screenshot_folder.setter
    def screenshot_folder(self, value: Path):
        self._settings.setValue("screenshot_folder", str(value))

    @property
    def image_format(self) -> ImageFormat:
        if (value := self._settings.value("image_format", defaultValue=None)) is None:
            return self._defaults.image_format
        return ImageFormat[value]

    @image_format.setter
    def image_format(self, value: ImageFormat):
        self._settings.setValue("image_format", value.name)

    @property
    def screenshot_hotkey(self) -> str:
        if (
            value := self._settings.value("screenshot_hotkey", defaultValue=None)
        ) is None:
            return self._defaults.screenshot_hotkey
        return value

    @screenshot_hotkey.setter
    def screenshot_hotkey(self, value: str):
        self._settings.setValue("screenshot_hotkey", value)

    def restore_defaults(self):
        for attribute, value in asdict(self._defaults).items():
            setattr(self, attribute, value)