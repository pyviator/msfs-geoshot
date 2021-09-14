from contextlib import contextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Iterable, Iterator, List

from PyQt5.QtCore import QAbstractNativeEventFilter
from pyqtkeybind import keybinder

if TYPE_CHECKING:
    from pyqtkeybind.win import WinKeyBinder


@dataclass
class Hotkey:
    key: str
    callback: Callable


class WindowsEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder: "WinKeyBinder"):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


HotkeysType = List[Hotkey]


class GlobalHotkeyService:
    def __init__(self, keybinder: "WinKeyBinder", window_id: int):
        self._keybinder = keybinder
        self._window_id = window_id
        self._hotkeys: HotkeysType = []

    @contextmanager
    def hotkeys_set(self, hotkeys: HotkeysType) -> Iterator[None]:
        self.set_hotkeys(hotkeys)
        yield
        self.remove_hotkeys()

    def set_hotkeys(self, hotkeys: HotkeysType):
        for hotkey in hotkeys:
            keybinder.register_hotkey(self._window_id, hotkey.key, hotkey.callback)
        self._hotkeys = hotkeys

    def remove_hotkeys(self):
        for hotkey in self._hotkeys:
            keybinder.unregister_hotkey(self._window_id, hotkey.key)
