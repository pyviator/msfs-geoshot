import sys
import traceback
from types import FrameType, TracebackType
from typing import NamedTuple, Optional, Type

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from .. import __app_name__


# cf. https://fman.io/blog/pyqt-excepthook/
class _FakeTraceback(NamedTuple):
    tb_frame: FrameType
    tb_lasti: int
    tb_lineno: int
    tb_next: Optional[TracebackType]


class ErrorHandler(QObject):
    exception_caught = pyqtSignal(str)

    def __call__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        tb_obj: TracebackType,
    ):
        if issubclass(type, KeyboardInterrupt):
            return sys.__excepthook__(exc_type, exc_value, tb_obj)

        new_tb_obj = self._add_missing_frames(tb_obj)

        error_str = "".join(traceback.format_exception(exc_type, exc_value, new_tb_obj))

        # TODO: Add links
        html = f"""<b>{__app_name__} encountered an error</b>.
Please report this message on GitHub or in the official support thread.<br><br>
<div style="white-space: pre-wrap">{error_str}</div>"""

        self.exception_caught.emit(html)

    def _add_missing_frames(self, tb_obj: TracebackType) -> TracebackType:
        new_tb_obj = _FakeTraceback(
            tb_obj.tb_frame, tb_obj.tb_lasti, tb_obj.tb_lineno, tb_obj.tb_next
        )
        frame = tb_obj.tb_frame.f_back

        while frame:
            new_tb_obj = _FakeTraceback(frame, frame.f_lasti, frame.f_lineno, new_tb_obj)  # type: ignore
            frame = frame.f_back

        return new_tb_obj  # type: ignore


class ErrorDialog(QDialog):
    def __init__(self, html: str, parent: Optional[QWidget] = None):
        parent = parent or QApplication.activeWindow()
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self._text_browser = QTextBrowser(self)
        self._text_browser.setOpenExternalLinks(True)
        self._text_browser.setHtml(html)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.button(QDialogButtonBox.StandardButton.Close).clicked.connect(  # type: ignore
            self.accept
        )
        self._copy_button = QPushButton("Copy to clipboard")
        self._copy_button.clicked.connect(self._on_copy_button)  # type: ignore
        button_box.addButton(self._copy_button, QDialogButtonBox.ButtonRole.ActionRole)

        layout.addWidget(self._text_browser)
        layout.addWidget(button_box)
        self.setLayout(layout)

        self.setWindowTitle(f"{__app_name__} Error")
        self.setMinimumHeight(300)
        self.setMinimumWidth(400)

    @pyqtSlot()
    def _on_copy_button(self):
        QApplication.clipboard().setText(self._text_browser.toPlainText())
        self._copy_button.setText("Copied!")


def show_error(html: str, parent: Optional[QWidget] = None):
    error_dialog = ErrorDialog(html, parent)
    error_dialog.exec()
