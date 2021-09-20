from typing import Optional
from PyQt5.QtCore import QObject, QThreadPool, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap

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
        pixmap = pixmap.scaledToHeight(self._thumbnail_height)
        return pixmap
