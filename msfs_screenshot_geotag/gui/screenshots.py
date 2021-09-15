from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, Optional

from PyQt5.QtGui import QGuiApplication, QImageWriter

from .. import __app_name__
from ..exif import ExifData
from ..names import FileNameComposer


class ImageFormat(Enum):
    JPG = "jpg"
    TIFF = "tiff"
    PNG = "png"


@dataclass
class _ImageFormatSettings:
    extension: str
    quality: Optional[int]
    compression: Optional[int]
    optimized_write: Optional[bool]
    progressive_scan_write: Optional[bool]


class ScreenshotService:

    _settings_by_image_format: Dict[ImageFormat, _ImageFormatSettings] = {
        # compression is in range 0,100, quality just maps to compression in reverse
        ImageFormat.PNG: _ImageFormatSettings(
            extension="png",
            quality=None,
            compression=100,
            optimized_write=True,
            progressive_scan_write=True,
        ),
        ImageFormat.JPG: _ImageFormatSettings(
            extension="jpg",
            quality=100,
            compression=None,
            optimized_write=None,
            progressive_scan_write=None,
        ),
        # compression is binary 0/1, quality is ignored
        ImageFormat.TIFF: _ImageFormatSettings(
            extension="tiff",
            quality=None,
            compression=1,
            optimized_write=None,
            progressive_scan_write=None,
        ),
    }

    def __init__(self, file_name_composer: FileNameComposer):
        self._file_name_composer = file_name_composer

    def take_screenshot(
        self,
        target_folder: Path,
        file_name_format: str,
        date_format: str,
        exif_data: Optional[ExifData] = None,
        image_format: ImageFormat = ImageFormat.JPG,
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

        self._grab_screenshot(out_path=out_path, image_format=image_format)

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

        extension = self._settings_by_image_format[image_format].extension
        truncated_file_stem = file_stem[:250]
        file_name = f"{truncated_file_stem}.{extension}"

        return file_name

    def _grab_screenshot(self, out_path: Path, image_format: ImageFormat):
        # TODO: identify actual window rather than using primary screen
        active_screen = QGuiApplication.primaryScreen()
        root_window_pixmap = active_screen.grabWindow(0)  # type: ignore
        image = root_window_pixmap.toImage()

        image_format_settings = self._settings_by_image_format[image_format]

        image_writer = QImageWriter()
        image_writer.setFileName(str(out_path))
        image_writer.setFormat(image_format.value.encode())

        if (compression := image_format_settings.compression) is not None:
            image_writer.setCompression(compression)
        if (quality := image_format_settings.quality) is not None:
            image_writer.setQuality(quality)
        if (optimized_write := image_format_settings.optimized_write) is not None:
            image_writer.setOptimizedWrite(optimized_write)
        if (
            progressive_scan_write := image_format_settings.progressive_scan_write
        ) is not None:
            image_writer.setProgressiveScanWrite(progressive_scan_write)

        image_writer.write(image)
