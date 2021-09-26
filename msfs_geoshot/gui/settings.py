from pathlib import Path
from typing import Optional

from PyQt5.QtCore import QObject, QSettings, QStandardPaths

from .. import __app_name__, __author__
from ..screenshots import ImageFormat

from dataclasses import dataclass, asdict


@dataclass
class _SettingsData:
    screenshot_folder: Path = (
        Path(QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)) / "MSFS"
    )
    image_format: ImageFormat = ImageFormat.JPEG
    screenshot_hotkey: str = "Ctrl+Shift+S"
    file_name_format: str = "MSFS_{datetime}_{geocode}"
    date_format: str = "%Y-%m-%d-%H%M%S"
    minimize_to_tray: bool = False
    play_sound: bool = True
    show_notification: bool = True


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

    # ---- General methods -----

    @property
    def defaults(self):
        return self._defaults

    def restore_defaults(self):
        for attribute, value in asdict(self._defaults).items():
            setattr(self, attribute, value)

    # ---- Settings getters/setters -----

    @property
    def screenshot_folder(self) -> Path:
        key = "screenshot_folder"
        if not self._settings.contains(key):
            return self._defaults.screenshot_folder
        return Path(self._settings.value(key, type=str))

    @screenshot_folder.setter
    def screenshot_folder(self, value: Path):
        self._settings.setValue("screenshot_folder", str(value))

    @property
    def image_format(self) -> ImageFormat:
        key = "image_format"
        if not self._settings.contains(key):
            return self._defaults.image_format
        return ImageFormat[self._settings.value(key, type=str)]

    @image_format.setter
    def image_format(self, value: ImageFormat):
        self._settings.setValue("image_format", value.name)

    @property
    def screenshot_hotkey(self) -> str:
        key = "screenshot_hotkey"
        if not self._settings.contains(key):
            return self._defaults.screenshot_hotkey
        return self._settings.value(key, type=str)

    @screenshot_hotkey.setter
    def screenshot_hotkey(self, value: str):
        self._settings.setValue("screenshot_hotkey", value)

    @property
    def file_name_format(self) -> str:
        key = "file_name_format"
        if not self._settings.contains(key):
            return self._defaults.file_name_format
        return self._settings.value(key, type=str)

    @file_name_format.setter
    def file_name_format(self, value: str):
        self._settings.setValue("file_name_format", value)

    @property
    def date_format(self) -> str:
        key = "date_format"
        if not self._settings.contains(key):
            return self._defaults.date_format
        return self._settings.value(key, type=str)

    @date_format.setter
    def date_format(self, value: str):
        self._settings.setValue("date_format", value)

    @property
    def minimize_to_tray(self) -> bool:
        key = "minimize_to_tray"
        if not self._settings.contains(key):
            return self._defaults.minimize_to_tray
        return self._settings.value(key, type=bool)

    @minimize_to_tray.setter
    def minimize_to_tray(self, value: bool):
        self._settings.setValue("minimize_to_tray", value)
    
    @property
    def play_sound(self) -> bool:
        key = "play_sound"
        if not self._settings.contains(key):
            return self._defaults.play_sound
        return self._settings.value(key, type=bool)

    @play_sound.setter
    def play_sound(self, value: bool):
        self._settings.setValue("play_sound", value)

    @property
    def show_notification(self) -> bool:
        key = "show_notification"
        if not self._settings.contains(key):
            return self._defaults.show_notification
        return self._settings.value(key, type=bool)

    @show_notification.setter
    def show_notification(self, value: bool):
        self._settings.setValue("show_notification", value)

    @property
    def times_launched(self) -> int:
        key = "internal/times_launched"
        if not self._settings.contains(key):
            return 0
        return self._settings.value(key, type=int)

    @times_launched.setter
    def times_launched(self, value: int):
        self._settings.setValue("internal/times_launched", value)
