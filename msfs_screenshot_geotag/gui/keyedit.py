from typing import Optional
from PyQt5.QtWidgets import QKeySequenceEdit
from PyQt5.QtGui import QKeyEvent, QKeySequence, QFocusEvent
from PyQt5.QtCore import Qt


class CustomKeySequenceEdit(QKeySequenceEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.editingFinished.connect(self._truncate_shortcut)
        self._last_shortcut: Optional[QKeySequence] = None
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

    def keyPressEvent(self, key_event: QKeyEvent) -> None:
        return super().keyPressEvent(key_event)

    def _truncate_shortcut(self):
        # Do not allow sequential shortcuts and make sure to fill out field
        # if empty
        sequence = self.keySequence()
        if not sequence:
            if self._last_shortcut:
                self.setKeySequence(self._last_shortcut)
            return
        value = sequence[0]
        new_shortcut = QKeySequence(value)
        self.setKeySequence(new_shortcut)

    def focusInEvent(self, focus_event: QFocusEvent) -> None:
        self._last_shortcut = self.keySequence()
        self.clear()
        return super().focusInEvent(focus_event)
