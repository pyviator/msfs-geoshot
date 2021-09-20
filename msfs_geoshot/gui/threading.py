from typing import Callable
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal


class Signals(QObject):
    success = pyqtSignal(object)
    error = pyqtSignal(object)
    done = pyqtSignal()


class Runner(QRunnable):
    def __init__(self, task: Callable, *args, **kwargs):
        super().__init__()
        self.signals = Signals()
        self._task = task
        self._args = args
        self._kwargs = kwargs

    def run(self):
        try:
            result = self._task(*self._args, **self._kwargs)
            self.signals.success.emit(result)
        except Exception as e:
            self.signals.error.emit(e)
        finally:
            self.signals.done.emit()
