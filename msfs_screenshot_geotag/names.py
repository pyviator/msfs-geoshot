from os import name
import string
import time
from datetime import date, datetime
from typing import Dict, List, NamedTuple, Optional, Tuple, cast

from pathvalidate import ValidationError, validate_filename
import tzlocal
from geopy.geocoders import Nominatim
from geopy.location import Location

from . import __app_name__
from .exif import ExifData


class FileNameField(NamedTuple):
    name: str
    required: bool
    description: str


_file_name_fields: List[FileNameField] = [
    FileNameField(
        name="datetime",
        required=True,
        description="Date and time string (e.g. '2022-01-01'). Exact format is governed by date format below.",
    ),
    FileNameField(
        name="geocode",
        required=False,
        description="""A human-readable description of the location the screenshot
was taken at (e.g. <i>USA-New_York-New_York_City</i>), as returned by <a href='https://wiki.openstreetmap.org/wiki/Nominatim'>
OSM Nominatim</a>.""",
    ),
]


class FileNameComposer:
    def __init__(self, user_agent: str):
        self._user_agent = user_agent

    def compose_name(
        self, name_format: str, date_format: str, exif_data: Optional[ExifData] = None
    ):
        is_valid_name_format, error = self.is_name_format_valid(name_format)
        if not is_valid_name_format:
            raise ValueError(f"Invalid format string provided: {error}")

        is_valid_date_format, error = self.is_date_format_valid(date_format)
        if not is_valid_date_format:
            raise ValueError(f"Invalid format string provided: {error}")

        format_data: Dict[str, Optional[str]] = {
            "datetime": self._get_datetime_string(date_format),
            "geocode": (
                self._maybe_get_geocode_string(exif_data) if exif_data else None
            )
            or "no-geocode-found",
        }

        return name_format.format(**format_data)

    def is_name_format_valid(self, name_format: str) -> Tuple[bool, str]:
        if not name_format:
            return False, "Name format must not be empty."

        try:
            mock_file_name = f"{name_format}.extension"
            validate_filename(mock_file_name)
        except ValidationError as e:
            return False, str(e)

        formatter = string.Formatter().parse(name_format)
        try:
            items = list(formatter)
        except ValueError:
            return False, "Format string is invalid."

        field_names = [name for text, name, spec, conv in items if name is not None]

        known_names = []
        for file_name_field in _file_name_fields:
            known_names.append(file_name_field.name)
            if file_name_field.required and file_name_field.name not in field_names:
                return False, f"Missing required field: {{{file_name_field.name}}}."

        for field_name in field_names:
            if field_name not in known_names:
                return False, f"Unrecognized field name: '{{{field_name}}}'"

        return True, ""

    def is_date_format_valid(self, date_format: str) -> Tuple[bool, str]:
        if not date_format:
            return False, "Date format must not be empty."

        try:
            mock_file_name = f"{date_format}.extension"
            validate_filename(mock_file_name)
        except ValidationError as e:
            return False, str(e)

        test_time = datetime.fromtimestamp(1631728655)
        try:
            formatted = test_time.strftime(date_format)
        except Exception:
            return False, "Date format could not be parsed."

        if formatted == "":
            return False, "Date format would result in empty string."

        if formatted == date_format:
            return False, "Date format does not contain any placeholders."

        return True, ""

    def get_supported_fields(self) -> List[FileNameField]:
        return _file_name_fields

    def _get_datetime_string(self, date_format: str) -> str:
        # TODO: Get from screenshot if available
        capture_time = time.time()
        local_timezone = tzlocal.get_localzone()
        capture_datetime = datetime.fromtimestamp(capture_time, tz=local_timezone)
        return capture_datetime.strftime(date_format)

    def _maybe_get_geocode_string(self, exif_data: ExifData) -> Optional[str]:
        try:
            geolocator = Nominatim(user_agent=self._user_agent)
            location: Location = cast(
                Location,
                geolocator.reverse(
                    (exif_data.GPSLatitude, exif_data.GPSLongitude),
                    language="en-US,en",
                    exactly_one=True,
                    zoom=10,  # limit to city region
                ),
            )
        except Exception as e:
            print(e)
            return None

        if not location or not getattr(location, "address", None):
            return None

        try:
            location_str = "-".join(reversed(location.address.split(", "))).replace(
                " ", "_"
            )
        except Exception as e:
            print(e)
            return None

        return location_str
