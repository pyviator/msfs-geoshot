# MSFS Screenshot GeoTag

import sys
from pathlib import Path

from msfs_screenshot_geotag import __version__, __app_name__
from msfs_screenshot_geotag.exif import ExifService
from msfs_screenshot_geotag.gui.app import Application
from msfs_screenshot_geotag.gui.main_window import MainWindow
from msfs_screenshot_geotag.gui.screenshots import ScreenShotService
from msfs_screenshot_geotag.sim import SimService


def run():
    app = Application(argv=sys.argv, name=__app_name__, version=__version__)
    sim_service = SimService()
    exif_service = ExifService()
    screenshot_service = ScreenShotService(
        sim_service=sim_service, exif_service=exif_service, target_folder=Path.home()
    )
    main_window = MainWindow(screenshot_service=screenshot_service)
    main_window.show()
    return app.exec()


sys.exit(run())
