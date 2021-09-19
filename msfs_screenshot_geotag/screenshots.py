from dataclasses import asdict, dataclass
from enum import Enum
from msfs_screenshot_geotag.windows import WindowRectangle
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
        name: str,
        window_rectangle: Optional[WindowRectangle] = None,
        image_format: ImageFormat = ImageFormat.JPEG,
    ) -> Path:
        if not target_folder.is_dir():
            target_folder.mkdir(parents=True, exist_ok=True)

        extension = image_format.value
        out_path = target_folder / f"{name}.{extension}"

        self._grab_screenshot(
            window_rectangle=window_rectangle,
            out_path=out_path,
            image_format=image_format,
        )

        return out_path

    def _grab_screenshot(
        self,
        window_rectangle: Optional[WindowRectangle],
        out_path: Path,
        image_format: ImageFormat,
    ):
        if window_rectangle:
            image = ImageGrab.grab(bbox=window_rectangle, all_screens=True)
        else:
            image = ImageGrab.grab()  # full screen

        image_format_settings = self._settings_by_image_format[image_format]
        image_format_settings_dict = asdict(image_format_settings)
        keyword_arguments = {
            key: value
            for key, value in image_format_settings_dict.items()
            if value is not None
        }

        image.save(str(out_path), format=image_format.name, **keyword_arguments)
