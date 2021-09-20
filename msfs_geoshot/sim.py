"""
Parts of this module are based on msfs-screenshot-gps-data by Luuk3333

Copyright (C) 2020 Luuk3333 <https://github.com/Luuk3333/msfs-screenshot-gps-data>

Used under the GNU Affero General Public License v3.0
"""

import time
import traceback
import warnings
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Set
import math

import psutil
from SimConnect import AircraftRequests, SimConnect

from .metadata import EXIF_DATE_FORMAT, EXIF_OFFSET_FORMAT, Metadata
from .time import (
    get_datetime_string,
    get_local_offset_delta,
    string_format_time_delta,
)
from .windows import get_window_ids_by_process_name, get_window_title_by_window_id


class SimServiceError(Exception):
    pass


@dataclass
class _RawSimData:
    # GPS
    latitude: Optional[float]  # degrees
    longitude: Optional[float]  # degrees
    altitude: Optional[float]  # m
    speed: Optional[float]  # m/s
    heading: Optional[float]  # aircraft (not camera!) heading, radians
    dest_latitude: Optional[float]
    dest_longitude: Optional[float]
    # Misc
    aircraft_type: Optional[bytes]


@dataclass
class _SimData:
    # GPS
    latitude: float  # degrees
    longitude: float  # degrees
    altitude: float  # m
    speed: float  # m/s
    heading: float
    dest_latitude: Optional[float]  # radians
    dest_longitude: Optional[float]  # radians
    # Misc
    aircraft_type: Optional[str]


_nullable_sim_data: Set[str] = set(("dest_latitude", "dest_longitude", "aircraft_type"))


class SimService:

    _sim_executable = "FlightSimulator.exe"
    _sim_window_title = "Microsoft Flight Simulator"

    def _is_sim_running(self) -> bool:
        return self._sim_executable in (p.name() for p in psutil.process_iter())

    def _is_user_in_flight(self, sim_location_data: _SimData) -> bool:
        return not (
            abs(sim_location_data.latitude) < 0.1
            and abs(sim_location_data.longitude) < 0.1
            and abs(sim_location_data.speed) < 0.1
        )

    def get_simulator_main_window_id(self) -> int:
        window_ids = get_window_ids_by_process_name(self._sim_executable)
        results: List[int] = []
        for window_id in window_ids:
            if self._sim_window_title in get_window_title_by_window_id(window_id):
                results.append(window_id)
        if len(results) > 1:
            raise SimServiceError("Could not uniquely identify main simulator window.")
        elif not results:
            raise SimServiceError("Could not find simulator window.")
        return results[0]

    def get_flight_data(self) -> Optional[Metadata]:
        if not self._is_sim_running():
            raise SimServiceError("Simulator is not running")

        try:
            sim_connect = SimConnect()
        except ConnectionError as e:
            traceback.print_exc()
            raise SimServiceError("Could not connect to SimConnect")

        aircraft_requests = AircraftRequests(sim_connect)

        raw_sim_location_data = _RawSimData(
            latitude=aircraft_requests.get("GPS_POSITION_LAT"),
            longitude=aircraft_requests.get("GPS_POSITION_LON"),
            altitude=aircraft_requests.get("GPS_POSITION_ALT"),
            speed=aircraft_requests.get("GPS_GROUND_SPEED"),
            heading=aircraft_requests.get("GPS_GROUND_TRUE_HEADING"),
            dest_latitude=aircraft_requests.get("GPS_WP_NEXT_LAT"),
            dest_longitude=aircraft_requests.get("GPS_WP_NEXT_LON"),
            aircraft_type=aircraft_requests.get("TITLE"),
        )
        # TITLE

        sim_connect.exit()

        null_values = {
            key: value
            for key, value in asdict(raw_sim_location_data).items()
            if key not in _nullable_sim_data and value is None
        }

        if null_values:
            raise SimServiceError(
                f"Got invalid location data from SimConnect for the following values: {null_values}"
            )

        sim_location_data_dict: Dict[str, Any] = {}

        for key, value in asdict(raw_sim_location_data).items():
            if isinstance(value, bytes):
                try:
                    value = value.decode("utf-8")
                except Exception:
                    value = value.decode("ascii")
            sim_location_data_dict[key] = value

        sim_location_data = _SimData(**sim_location_data_dict)

        if not self._is_user_in_flight(sim_location_data):
            warnings.warn("User is not currently in flight.")
            return None

        return self._sim_location_to_metadata(sim_location_data)

    def _sim_location_to_metadata(self, sim_location_data: _SimData) -> Metadata:
        description = sim_location_data.aircraft_type
        capture_time = time.time()

        datetime_string = get_datetime_string(
           capture_time, date_format=EXIF_DATE_FORMAT
        )
        offset_timedelta = get_local_offset_delta()
        offset_time = string_format_time_delta(offset_timedelta, EXIF_OFFSET_FORMAT)

        return Metadata(
            # Internal
            capture_time = capture_time,
            # Date
            AllDates=datetime_string,
            OffsetTime=offset_time,
            # GPS
            GPSLatitude=round(sim_location_data.latitude, 5),
            GPSLongitude=round(sim_location_data.longitude, 5),
            GPSAltitude=round(sim_location_data.altitude, 2),
            GPSSpeed=round(sim_location_data.speed * 3.6, 2),  # m/s to km/h
            GPSImgDirection=round(math.degrees(sim_location_data.heading), 5),
            GPSDestLongitude=round(sim_location_data.dest_longitude, 5)
            if sim_location_data.dest_longitude
            else None,
            GPSDestLatitude=round(sim_location_data.dest_latitude, 5)
            if sim_location_data.dest_latitude
            else None,
            # MISC
            Description=description,
            ImageDescription=description,
        )
