import time
import traceback
import warnings
from dataclasses import asdict, dataclass
from typing import Optional

import psutil
from SimConnect import AircraftRequests, SimConnect

from .exif import ExifLocationData


class SimServiceError(Exception):
    pass


@dataclass
class RawSimLocationData:
    latitude: Optional[float]  # degrees
    longitude: Optional[float]  # degrees
    altitude: Optional[float]  # m
    speed: Optional[float]  # m/s


@dataclass
class SimLocationData:
    latitude: float  # degrees
    longitude: float  # degrees
    altitude: float  # m
    speed: float  # m/s
    time: float  # s since epoch


class SimService:

    _sim_executable = "FlightSimulator.exe"

    def _is_sim_running(self) -> bool:
        return self._sim_executable in (p.name() for p in psutil.process_iter())

    def _is_user_in_flight(self, sim_location_data: SimLocationData) -> bool:
        return (
            sim_location_data.latitude >= 0.1
            and sim_location_data.longitude >= 0.1
            and sim_location_data.speed >= 0.1
        )

    def get_current_location(self) -> Optional[ExifLocationData]:
        if not self._is_sim_running():
            raise SimServiceError("Simulator is not running")

        try:
            sim_connect = SimConnect()
        except ConnectionError as e:
            traceback.print_exc()
            raise SimServiceError("Could not connect to SimConnect")
        
        aircraft_requests = AircraftRequests(sim_connect)

        raw_sim_location_data = RawSimLocationData(
            latitude=aircraft_requests.get("GPS_POSITION_LAT"),
            longitude=aircraft_requests.get("GPS_POSITION_LON"),
            altitude=aircraft_requests.get("GPS_POSITION_ALT"),
            speed=aircraft_requests.get("GPS_GROUND_SPEED"),
        )

        sim_connect.exit()

        null_values = {
            key: value
            for key, value in asdict(raw_sim_location_data).items()
            if value is None
        }

        if null_values:
            raise SimServiceError(
                f"Got invalid location data from SimConnect for the following values: {null_values}"
            )

        sim_location_data = SimLocationData(
            **asdict(raw_sim_location_data), time=time.time()
        )

        if not self._is_user_in_flight(sim_location_data):
            warnings.warn("User is not currently in flight.")
            return None

        return self._sim_location_to_exif_location(sim_location_data)

    def _sim_location_to_exif_location(
        self, sim_location_data: SimLocationData
    ) -> ExifLocationData:
        return ExifLocationData(
            gps_datestamp=round(sim_location_data.time),
            gps_latitude=round(sim_location_data.latitude, 5),
            gps_longitude=round(sim_location_data.longitude, 5),
            gps_altitude=round(sim_location_data.altitude, 2),
            gps_speed=round(sim_location_data.speed * 3.6, 2),  # m/s to km/h
        )
