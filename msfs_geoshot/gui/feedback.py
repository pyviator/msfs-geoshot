from typing import Optional

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QLabel, QWidget

from .. import __app_name__, __issues_tracker__, __store_url__
from .forms.feedback import Ui_FeedbackDialog
from .util import open_url


class FeedbackDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._form = Ui_FeedbackDialog()
        self._form.setupUi(self)

        self._form.buttonBox.hide()
        self._form.happy_cta.hide()
        self._form.sad_cta.hide()

        self._form.happy.clicked.connect(self._form.intro.hide)
        self._form.happy.clicked.connect(self._form.happy_cta.show)
        self._form.happy.clicked.connect(self._form.buttonBox.show)
        self._form.sad.clicked.connect(self._form.intro.hide)
        self._form.sad.clicked.connect(self._form.buttonBox.show)
        self._form.sad.clicked.connect(self._form.sad_cta.show)

        self._form.rate.clicked.connect(lambda: open_url(__store_url__))
        self._form.feedback.clicked.connect(lambda: open_url(__issues_tracker__))

        for label in ("intro_label", "happy_label"):
            widget: QLabel = getattr(self._form, label)
            widget.setText(widget.text().format(__app_name__=__app_name__))

        self.resize(QSize(400, 140))
