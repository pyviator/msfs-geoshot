from abc import abstractmethod
from typing import Optional, Tuple
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QColor, QPalette, QValidator
from PyQt5.QtWidgets import QLabel, QLineEdit
from ..names import FileNameComposer
from .notification import NotificationColor

class _BaseValidator(QValidator):
    def __init__(
        self,
        line_edit: QLineEdit,
        warning_label: QLabel,
        file_name_composer: FileNameComposer,
        parent: Optional[QObject] = None,
    ):
        super().__init__(parent)
        self._line_edit = line_edit
        self._warning_label = warning_label
        self._file_name_composer = file_name_composer
        self._valid_palette = self._line_edit.palette()

        invalid_palette = QPalette()
        invalid_palette.setColor(QPalette.Base, QColor(NotificationColor.error.value))

        self._invalid_palette = invalid_palette

    def validate(self, input: str, position: int) -> Tuple[QValidator.State, str, int]:
        is_input_valid, error = self._validate(input)
        if is_input_valid:
            self._warning_label.hide()
            self._line_edit.setPalette(self._valid_palette)
            return QValidator.State.Acceptable, input, position
        else:
            self._warning_label.setText(f"<b>Error:</b>: {error}")
            self._warning_label.show()
            self._line_edit.setPalette(self._invalid_palette)
            return QValidator.State.Intermediate, input, position

    @abstractmethod
    def _validate(self, input: str) -> Tuple[bool, str]:
        pass


class FileNameFormatValidator(_BaseValidator):
    def _validate(self, input: str) -> Tuple[bool, str]:
        return self._file_name_composer.is_name_format_valid(input)


class DateFormatValidator(_BaseValidator):
    def _validate(self, input: str) -> Tuple[bool, str]:
        return self._file_name_composer.is_date_format_valid(input)
