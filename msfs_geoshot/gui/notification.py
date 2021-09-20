from enum import Enum
from typing import Callable, Optional

from PyQt5.QtCore import QObject, QPoint, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QCursor, QMouseEvent
from PyQt5.QtWidgets import QApplication, QLabel, QWidget


class NotificationColor(Enum):
    success = "#90ee90"
    error = "#ffcccb"
    neutral = "#e6e6e6"


class ScreenPolicy(Enum):
    show_on_primary_screen = 0  # screen window was spawned on
    show_on_active_screen = 1  # screen with mouse cursor


class NotificationHandler(QObject):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self._parent = parent
        self._timer: Optional["QTimer"] = None
        self._notification: Optional["Notification"] = None

    def notify(
        self,
        message: str,
        color: NotificationColor = NotificationColor.success,
        timeout: int = 2000,
        onclick: Optional[Callable] = None,
        screen_policy: ScreenPolicy = ScreenPolicy.show_on_active_screen,
    ):
        self.close_notification()

        self._notification = Notification(
            message=message, color=color.value, screen_policy=screen_policy
        )

        if onclick:
            self._notification.clicked.connect(onclick)

        self._timer = QTimer.singleShot(timeout, self.close_notification)
        self._notification.show()

    def close_notification(self):
        if self._notification:
            self._notification.close()
            self._notification = None
        if self._timer:
            self._timer.stop()
            self._timer.deleteLater()
            self._timer = None


class Notification(QLabel):
    clicked = pyqtSignal()

    def __init__(
        self,
        message: str,
        color: str,
        parent: Optional[QWidget] = None,
        screen_policy: ScreenPolicy = ScreenPolicy.show_on_active_screen
    ):
        super().__init__(parent=parent)
        self.setWindowFlags(Qt.WindowType.ToolTip)
        self.setStyleSheet(
            f"""
QLabel {{
    background-color: {color};
    margin: 10px;
    font-size: 10pt;
}}
"""
        )
        self.setText(message)
        if screen_policy.show_on_active_screen:
            global_cursor_position = QCursor.pos()
            desktop_widget = QApplication.desktop()
            mouse_screen_index = desktop_widget.screenNumber(global_cursor_position)
            mouse_screen_geometry = desktop_widget.screenGeometry(mouse_screen_index)
            self.move(QPoint(mouse_screen_geometry.x(), mouse_screen_geometry.y()))
        else:
            self.move(QPoint(0, 0))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        event.accept()
        self.clicked.emit()
        self.close()
