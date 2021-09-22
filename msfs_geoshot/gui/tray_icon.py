from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from .. import __app_name__
from .main_window import MainWindow


class AppTrayIcon(QSystemTrayIcon):
    def __init__(self, icon: QIcon, main_window: MainWindow):
        super().__init__(icon, main_window)
        self._main_window = main_window
        self.activated.connect(self._on_activated)  # type: ignore
        self.setToolTip(__app_name__)

        menu = QMenu(main_window)
        action = menu.addAction(f"Show {__app_name__}")
        action.triggered.connect(self._show_main_window)  # type: ignore

        menu.addSeparator()

        action = menu.addAction("Quit")
        action.triggered.connect(QApplication.exit)  # type: ignore

        self.setContextMenu(menu)

    def _on_activated(self, activation_reason: QSystemTrayIcon.ActivationReason):
        if activation_reason == QSystemTrayIcon.ActivationReason.Context:
            return
        if self._main_window.isVisible() and not self._main_window.isMinimized():
            self._main_window.showMinimized()
        else:
            self._show_main_window()

    def _show_main_window(self):
        self._main_window.showNormal()
        self._main_window.raise_()
        self._main_window.activateWindow()
