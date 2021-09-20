import time

from .metadata import EXIF_DATE_FORMAT, Metadata
from .time import get_datetime_string
from .windows import WindowRectangle


def get_mock_metadata() -> Metadata:
    capture_time = time.time()
    return Metadata(
        capture_time=capture_time,
        AllDates=get_datetime_string(capture_time, EXIF_DATE_FORMAT),
        OffsetTime="+01:00",
        GPSLatitude=60,
        GPSLongitude=60,
        GPSAltitude=100,
        GPSSpeed=200,
        GPSImgDirection=0,
    )


def get_mock_window_rectangle() -> WindowRectangle:
    return WindowRectangle(0, 0, 1920, 1200)
