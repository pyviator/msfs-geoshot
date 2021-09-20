from typing import Optional

from PyQt5.QtCore import QObject, QSize, Qt, QThreadPool, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QMouseEvent, QPixmap
from PyQt5.QtWidgets import QFrame, QLabel, QWidget

from .threading import Runner


class ThumbnailMaker(QObject):
    thumb_ready = pyqtSignal(QPixmap)

    def __init__(
        self,
        thread_pool: QThreadPool,
        thumbnail_height: int,
        parent: Optional[QObject] = None,
    ):
        super().__init__(parent)
        self._thread_pool = thread_pool
        self._thumbnail_height = thumbnail_height

    @pyqtSlot(str)
    def create_thumbnail(self, path: str):
        runner = Runner(self._create_thumbnail, path)
        runner.signals.success.connect(self._on_thumb_ready)  # type: ignore

        self._thread_pool.start(runner)

    @pyqtSlot(object)
    def _on_thumb_ready(self, pixmap: QPixmap):
        self.thumb_ready.emit(pixmap)

    def _create_thumbnail(self, path) -> QPixmap:
        pixmap = QPixmap()
        pixmap.load(path)
        pixmap = pixmap.scaledToHeight(
            self._thumbnail_height, Qt.TransformationMode.SmoothTransformation
        )
        return pixmap


class ThumbnailWidget(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setFrameShadow(QFrame.Sunken)
        self.setMinimumSize(QSize(170, 96))
        self.setMaximumSize(QSize(16777215, 96))
        self.setFrameShape(QFrame.Box)
        self.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.setObjectName("thumbnail")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.clicked.emit()
        return super().mousePressEvent(event)
