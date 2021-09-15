from abc import abstractmethod
from typing import Optional, Tuple

from PyQt5.QtCore import QObject, Qt, pyqtSlot
from PyQt5.QtGui import QColor, QPalette, QValidator
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton

from ..names import FileNameComposer
from .notification import NotificationColor

# TODO: Refactor into a group widget consisting of label, line edit, button
# and controlled by validator

class _BaseValidator(QValidator):
    def __init__(
        self,
        line_edit: QLineEdit,
        warning_label: QLabel,
        save_button: QPushButton,
        file_name_composer: FileNameComposer,
        parent: Optional[QObject] = None,
    ):
        super().__init__(parent)
        self._line_edit = line_edit
        self._warning_label = warning_label
        self._save_button = save_button
        self._file_name_composer = file_name_composer

        self._valid_palette= QPalette()
        self._valid_palette.setColor(QPalette.Base, QColor(NotificationColor.success.value))

        self._invalid_palette = QPalette()
        self._invalid_palette.setColor(QPalette.Base, QColor(NotificationColor.error.value))

        self._warning_label.hide()
        self._save_button.setDisabled(True)

        self._last_input: Optional[str] = self._line_edit.text()

    def validate(self, input: str, position: int) -> Tuple[QValidator.State, str, int]:
        is_input_valid, error = self._validate(input)
        if is_input_valid:
            if input != self._last_input:
                self._warning_label.hide()
                self._line_edit.setPalette(self._valid_palette)
                self._save_button.setEnabled(True)
            self._last_input = input
            return QValidator.State.Acceptable, input, position
        else:
            self._warning_label.setText(f"<b>Error</b>: {error}")
            self._warning_label.show()
            self._line_edit.setPalette(self._invalid_palette)
            self._save_button.setDisabled(True)
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
