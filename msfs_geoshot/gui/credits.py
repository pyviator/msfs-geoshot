from typing import Optional

from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from .. import (
    LICENSES_PATH,
    __app_name__,
    __author__,
    __copyright_year__,
    __version__,
    __author_link__,
)


class CreditsDialog(QDialog):

    _licenses_media = LICENSES_PATH / "licenses_media.txt"
    _licenses_binaries = LICENSES_PATH / "licenses_binaries.txt"
    _licenses_pypi = LICENSES_PATH / "licenses_pypi.txt"
    _license_app = LICENSES_PATH / "license.txt"

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        text_browser = QTextBrowser(self)
        text_browser.setOpenExternalLinks(True)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.button(QDialogButtonBox.StandardButton.Ok).clicked.connect(  # type: ignore
            self.accept
        )

        layout.addWidget(text_browser)
        layout.addWidget(button_box)

        text_browser.setHtml(self._compose_credit_text())

        self.setWindowTitle(f"About {__app_name__}")
        self.setMinimumHeight(500)
        self.setMinimumWidth(500)

    def _compose_credit_text(self) -> str:
        with self._license_app.open(encoding="utf-8") as license_file:
            app_license_text = license_file.read()

        with self._licenses_pypi.open(encoding="utf-8") as licenses_file:
            pypi_licenses_text = licenses_file.read()

        with self._licenses_binaries.open(encoding="utf-8") as licenses_file:
            binaries_licenses_text = licenses_file.read()

        with self._licenses_media.open(encoding="utf-8") as licenses_file:
            media_licenses_text = licenses_file.read()

        credits_text = f"""

<h1>{__app_name__} Version {__version__}</h1>

<div style="font-size: 12pt">
<p><b>{__app_name__}</b> is Copyright (C) {__copyright_year__} <a href="{__author_link__}">{__author__}</a></p>

<p>The source code for {__app_name__} is available on
<a href="https://github.com/pyviator/msfs-geoshot">GitHub</a>.
Contributions are welcome!</p>
</div>

<div style="font-size: 10pt">

<p><em>Regarding {__app_name__}&#39;s code</em>:</p>

<p>This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.</p>

<p>This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.</p>

<p><em>Regarding non-code-files</em>:</p>

{media_licenses_text}

<p>Compiled builds of MSFS GeoShot include <a href="https://github.com/odwdinc/Python-SimConnect/">Python-SimConnect</a> 
which ships with a bundled version of the SimConnect.dll from Microsoft Flight Simulator&#39;s SDK. 
Microsoft Flight Simulator is © Microsoft Corporation. Any assets from Microsoft Flight Simulator 
used by MSFS GeoShot (SimConnect.dll) are used under Microsoft&#39;s &quot;Game Content Usage Rules&quot;. 
This project is not in any way endorsed by or affiliated with Microsoft.</p>

<p>{__app_name__} is built on the shoulder of giants, with a special shout-out
due for the following members of the MSFS community:</p>

<ul>
 <li><a href="https://github.com/odwdinc">odwdinc</a> for their work on <a href="https://github.com/odwdinc/Python-SimConnect">Python-SimConnect</a></li>
 <li><a href="https://github.com/Luuk3333/msfs-screenshot-gps-data">Luuk3333</a> for inspiring this project with <a href="https://github.com/Luuk3333/msfs-screenshot-gps-data">msfs-screenshot-gps-data</a></li>
</ul>

<p>{__app_name__} would also not exist without a number of other third-party software 
in the greater open-source ecosystem. A full overview of each dependency and their
copyright notices and licenses follows below after {__app_name__}'s full license text.</p>
</div>

<hr/>

<h2>Copyright Notices and License Texts</h2>

<h3>{__app_name__}</h3>

<div style="white-space: pre-wrap">
{app_license_text}
</div>

<hr/>

<h3>Bundled Third-party Open-Source Software</h3>

<div style="white-space: pre-wrap">
<br>
{binaries_licenses_text}
<br>
{pypi_licenses_text}
</div>
"""

        return credits_text


def show_credits(parent: Optional[QWidget] = None):
    credits_dialog = CreditsDialog(parent)
    credits_dialog.exec()
