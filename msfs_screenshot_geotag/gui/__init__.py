
import sys

from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher
from pyqtkeybind import keybinder

from ..sim_service import SimService

if TYPE_CHECKING:
    from pyqtkeybind.win import WinKeyBinder

class WindowsEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder: "WinKeyBinder"):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0

def take_screenshot():
    pass
    # QGuiApplication.primaryScreen().grabWindow(0).save("hello.png", quality=100)

def run_app():
    app = QApplication(sys.argv)
    app.setApplicationName("MSFS Screenshot GeoTag")
    main_window = QMainWindow()
    main_window.setWindowTitle("MSFS Screenshot GeoTag")
    
    central_widget = QWidget(main_window)
    central_layout = QVBoxLayout(central_widget)
    main_window.setCentralWidget(central_widget)

    sim_service = SimService()

    location = sim_service.get_current_location()

    central_layout.addWidget(QLabel("My label", parent=central_widget))
    central_layout.addWidget(QPushButton("My button", parent=central_widget))
    
    def callback():
        print("hello world")

    
    keybinder.init()
    window_id = main_window.winId()
    keybinder.register_hotkey(window_id, "Shift+Ctrl+A", callback)

    windows_event_filter = WindowsEventFilter(keybinder)  # type: ignore

    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(windows_event_filter)

    main_window.show()
    app.exec()

    try:
        keybinder.unregister_hotkey(window_id, "Shift+Ctrl+A")
    except Exception as e:
        print(e)

run_app()
