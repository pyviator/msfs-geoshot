from typing import List
from PyQt5.QtWidgets import QApplication

class Application(QApplication):

    def __init__(self, argv: List[str], name: str, version: str):
        super().__init__(argv)
        self.setApplicationName(name)
        self.setApplicationVersion(version)
