from typing import TypedDict, Literal, Dict, Union, Tuple
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

from src.shadcn_for_pyqt.theming.colors import TailwindColors


type WidgetSizeDict = Dict[Literal["width", "height"], int]
type WidgetSize = Union[Tuple[int, int], WidgetSizeDict]



class WidgetSettings(TypedDict):
    background_color: str
    size: WidgetSize


class BaseWidget(QWidget):
    def __init__(self, parent=None, settings: WidgetSettings = None, *args, **kwargs):
        super(BaseWidget, self).__init__(parent, *args, **kwargs)
        self._setup(settings or {})

    def set_size(self, width, height):
        self.setFixedSize(width, height)

    def background(self):
        return self._settings['background_color']

    def set_background(self, color):
        self._settings['background_color'] = color

    def _setup(self, settings: WidgetSettings):
        self._settings = settings

        if 'background_color' not in settings:
            self._settings.setdefault('background_color', TailwindColors.slate.tw_slate_50)

        if 'size' not in settings:
            self._settings.setdefault('size', {
                'width': 100,
                'height': 100
            })

        if isinstance(settings['size'], tuple):
            self._settings.setdefault('size', {
                'width': settings['size'][0],
                'height': settings['size'][1]
            })

        self.set_size(
            self._settings['size']['width'],
            self._settings['size']['height']
        )

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet(f"""
            background-color: {self._settings['background_color']};
        """)
