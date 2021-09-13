from dataclasses import dataclass, field
from typing import Literal, Union
from pathlib import Path


@dataclass
class ExifLocationData:
    gps_datestamp: int
    gps_latitude: float
    gps_longitude: float
    gps_altitude: float
    gps_speed: float
    # --- Computed ---:
    gps_latitude_ref: Union[Literal["N"], Literal["S"]] = field(init=False)
    gps_longitude_ref: Union[Literal["E"], Literal["W"]] = field(init=False)
    # below sea level, above sea level
    gps_altitude_ref: Union[Literal[0], Literal[1]] = field(init=False)
    # --- Constant ---:
    # km/h, mph, knots
    gps_speed_ref: Union[Literal["K"], Literal["M"], Literal["N"]] = field(init=False)

    def __post_init__(self):
        self.gps_longitude_ref = "E" if self.gps_longitude >= 0 else "W"
        self.gps_latitude_ref = "N" if self.gps_latitude >= 0 else "S"
        self.gps_altitude_ref = 1 if self.gps_altitude >= 0 else 0
        self.gps_speed_ref = "K"



class ExifLocationService:
    def write_data(self, exif_location_data: ExifLocationData, image: Path):
        pass
