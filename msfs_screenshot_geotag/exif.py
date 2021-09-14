from dataclasses import asdict, dataclass, field
from typing import Literal, Union
from pathlib import Path
from exif import Image
import exif


@dataclass
class ExifLocationData:
    # FIXME: add GPSVersionID to let images be recognized bey GeoSetter
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
        self.gps_altitude_ref = 0 if self.gps_altitude >= 0 else 1
        self.gps_speed_ref = "K"


class ExifService:
    def write_data(
        self,
        image_path: Path,
        exif_location_data: ExifLocationData,
    ):
        with image_path.open("rb") as image_file:
            image = Image(image_file)

        print(image.list_all())

        # image.gps_datestamp = exif_location_data.gps_datestamp
        image.gps_latitude = exif_location_data.gps_latitude
        image.gps_longitude = exif_location_data.gps_longitude
        image.gps_altitude = exif_location_data.gps_altitude
        image.gps_speed = exif_location_data.gps_speed
        image.gps_latitude_ref = exif_location_data.gps_latitude_ref
        image.gps_longitude_ref = exif_location_data.gps_longitude_ref
        image.gps_altitude_ref = exif_location_data.gps_altitude_ref
        image.gps_speed_ref = exif_location_data.gps_speed_ref

        image_path.unlink()

        with image_path.open("wb") as new_image_file:
            new_image_file.write(image.get_file())
