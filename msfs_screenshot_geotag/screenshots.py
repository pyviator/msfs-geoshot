from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, Optional

import win32gui
from PIL import ImageGrab

from . import __app_name__
from .exif import ExifData
from .names import FileNameComposer


class ImageFormat(Enum):
    JPEG = "jpg"
    TIFF = "tiff"
    PNG = "png"


@dataclass
class _ImageFormatSettings:
    quality: Optional[int] = None
    compression: Optional[str] = None
    compress_level: Optional[int] = None
    optimize: Optional[bool] = None
    progressive: Optional[bool] = None


class ScreenshotService:

    _settings_by_image_format: Dict[ImageFormat, _ImageFormatSettings] = {
        ImageFormat.PNG: _ImageFormatSettings(
            # optimize would imply compress_level=9
            compress_level=6,
        ),
        ImageFormat.JPEG: _ImageFormatSettings(
            quality=100,
            optimize=True,
            progressive=True,  
        ),
        ImageFormat.TIFF: _ImageFormatSettings(
            compression="tiff_adobe_deflate",  # equivalent to ZIP. alternative: lzwa
        ),
    }

    def __init__(self, file_name_composer: FileNameComposer):
        self._file_name_composer = file_name_composer

    def take_screenshot(
        self,
        target_folder: Path,
        file_name_format: str,
        date_format: str,
        window_id: int = 0,
        exif_data: Optional[ExifData] = None,
        image_format: ImageFormat = ImageFormat.JPEG,
    ) -> Path:
        if not target_folder.is_dir():
            target_folder.mkdir(parents=True, exist_ok=True)

        screenshot_name = self._get_screenshot_name(
            file_name_format=file_name_format,
            date_format=date_format,
            image_format=image_format,
            exif_data=exif_data,
        )

        out_path = target_folder / screenshot_name

        self._grab_screenshot(
            window_id=window_id, out_path=out_path, image_format=image_format
        )

        return out_path

    def _get_screenshot_name(
        self,
        file_name_format: str,
        date_format: str,
        image_format: ImageFormat,
        exif_data: Optional[ExifData],
    ) -> str:
        file_stem = self._file_name_composer.compose_name(
            name_format=file_name_format,
            date_format=date_format,
            exif_data=exif_data,
        )

        extension = image_format.value
        truncated_file_stem = file_stem[:250]
        file_name = f"{truncated_file_stem}.{extension}"

        return file_name

    def _grab_screenshot(
        self, window_id: int, out_path: Path, image_format: ImageFormat
    ):
        win32gui.SetForegroundWindow(window_id)  # type: ignore
        bounding_box = win32gui.GetWindowRect(window_id)  # type: ignore
        image = ImageGrab.grab(bounding_box, all_screens=True)
        
        image_format_settings = self._settings_by_image_format[image_format]
        image_format_settings_dict = asdict(image_format_settings)
        keyword_arguments = {
            key: value
            for key, value in image_format_settings_dict.items()
            if value is not None
        }

        image.save(str(out_path), format=image_format.name, **keyword_arguments)