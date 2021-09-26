from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices


def open_url(url: str):
    QDesktopServices.openUrl(QUrl(url))
