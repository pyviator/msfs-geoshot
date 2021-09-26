import time

from PyQt5.QtCore import QCoreApplication, QUrl
from PyQt5.QtGui import QDesktopServices, QGuiApplication


def open_url(url: str):
    QDesktopServices.openUrl(QUrl(url))


def wait(duration: float):
    """Sleep for a set number of seconds without blocking main UI thread"""
    steps = int(duration * 10)
    for _ in range(steps):
        QGuiApplication.processEvents()
        time.sleep(0.1)
