from dataclasses import dataclass
from enum import Enum
from msfs_screenshot_geotag import DEBUG
from typing import TYPE_CHECKING, Dict, Optional
from PyQt5 import sip

from PyQt5.QtCore import QAbstractNativeEventFilter, QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget
from pyqtkeybind import keybinder

if TYPE_CHECKING:
    from pyqtkeybind.win import WinKeyBinder


class WindowsEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder: "WinKeyBinder"):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


class HotkeyID(Enum):
    take_screenshot = 0


@dataclass
class _StoredHotkey:
    key: str
    window: QWidget
    window_id: int


class GlobalHotkeyService(QObject):

    take_screenshot_pressed = pyqtSignal()

    def __init__(self, keybinder: "WinKeyBinder", parent: Optional[QObject] = None):
        super().__init__(parent)
        self._keybinder = keybinder
        self._hotkeys: Dict[HotkeyID, _StoredHotkey] = {}

    def bind_hotkey(self, hotkey_id: HotkeyID, key: str, window: QWidget):
        if hotkey_id in self._hotkeys:
            self.unbind_hotkey(hotkey_id)

        window_id = window.winId()

        keybinder.register_hotkey(
            window_id, key, lambda: self.send_hotkey_signal(hotkey_id)
        )

        self._hotkeys[hotkey_id] = _StoredHotkey(
            key=key, window=window, window_id=window_id  # type: ignore
        )

    def unbind_hotkey(self, hotkey_id: HotkeyID):
        if (hotkey := self._hotkeys.get(hotkey_id)) is None:
            return

        window_ids = [hotkey.window_id]

        window = hotkey.window
        if not sip.isdeleted(window):
            window_ids.append(window.winId())  # type: ignore

        for window_id in window_ids:
            try:
                keybinder.unregister_hotkey(window_id, hotkey.key)
                if DEBUG:
                    print(f"Unbound hotkey for {window_id}")
            except Exception as e:
                if DEBUG:
                    print(f"Could not unbind hotkey for {window_id}")
                pass

    def send_hotkey_signal(self, hotkey_id: HotkeyID):
        signal = getattr(self, f"{hotkey_id.name}_pressed")
        signal.emit()

    def unbind_all_hotkeys(self):
        print("Unbinding all")
        for hotkey_id in self._hotkeys.keys():
            self.unbind_hotkey(hotkey_id)
