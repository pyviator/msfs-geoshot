from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import QObject, QPoint, Qt, QTimer

from typing import Optional



class NotificationHandler(QObject):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self._parent = parent
        self._timer: Optional["QTimer"] = None
        self._notification: Optional["Notification"] = None

    def notify(self, message: str, color: str = "#90ee90", timeout: int = 2000):
        self.close_notification()
        
        self._notification = Notification(message=message, color=color, parent=self._parent)
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
    def __init__(self, message: str, color: str, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.setWindowFlags(Qt.WindowType.ToolTip)
        self.setStyleSheet(f"""
QLabel {{
    background-color: {color};
    margin: 10px;
    font-size: 10pt;
}}
""")
        self.setText(message)
        self.move(QPoint(0, 0))
