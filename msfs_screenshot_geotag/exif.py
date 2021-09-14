import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Literal, Union

from . import DEBUG


@dataclass
class ExifData:
    GPSLatitude: float
    GPSLongitude: float
    GPSAltitude: float
    GPSSpeed: float
    # --- Computed ---:
    GPSLatitudeRef: Literal["N", "S"] = field(init=False)
    GPSLongitudeRef: Literal["E", "W"] = field(init=False)
    GPSAltitudeRef: Literal[0, 1] = field(
        init=False
    )  # below sea level, above sea level
    # --- Constant ---:
    GPSSpeedRef: Literal["K", "M", "N"] = field(init=False)  # km/h, mph, knots

    def __post_init__(self):
        self.GPSLongitudeRef = "E" if self.GPSLongitude >= 0 else "W"
        self.GPSLatitudeRef = "N" if self.GPSLatitude >= 0 else "S"
        self.GPSAltitudeRef = 0 if self.GPSAltitude >= 0 else 1
        self.GPSSpeedRef = "K"


class ExifService:

    _exiftool = Path(__file__).parent / "_bin" / "exiftool.exe"

    def write_data(
        self,
        image_path: Path,
        exif_data: ExifData,
    ) -> bool:
        arguments = ["-n", "-overwrite_original"]

        if DEBUG:
            arguments.append("-verbose")

        for attribute, value in asdict(exif_data).items():
            if value == -999999:
                print(f"Invalid value {value} for attribute {attribute}. Skipping.")
                continue
            arguments.append(f"-{attribute}={value}")

        command_line = [str(self._exiftool)] + arguments + [str(image_path)]

        if DEBUG:
            print(command_line)

        try:
            output = subprocess.check_output(command_line, text=True)
            if DEBUG:
                print(output)
        except subprocess.CalledProcessError as e:
            print(e.output)
            return False
        except subprocess.SubprocessError as e:
            print(e)
            return False
        except Exception as e:
            raise e

        return True
