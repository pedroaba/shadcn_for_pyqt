import uuid
from typing import TypedDict, Literal, Dict, Union, Tuple, Optional
from enum import Enum
from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtCore import Qt

from src.shadcn_for_pyqt.theming.colors import TailwindColors


class ResponsiveOptions(Enum):
    WIDTH_MATCH_PARENT = "match_parent"
    HEIGHT_MATCH_PARENT = "match_parent"
    WIDTH_WRAP_CONTENT = "wrap_content"
    HEIGHT_WRAP_CONTENT = "wrap_content"
    SIZE_FILL_PARENT = "fill_parent"
    SIZE_FILL_CONTENT = "fill_content"


type WidgetSizeDict = Dict[Literal["width", "height"], int]
type WidgetSize = Union[Tuple[int, int], WidgetSizeDict]


class WidgetCorner(TypedDict):
    right: int
    left: int
    top: int
    bottom: int


class WidgetSettings(TypedDict):
    background_color: Optional[str]
    size: Optional[WidgetSize]
    corner: Optional[WidgetCorner]
    responsive_width: Optional[ResponsiveOptions]
    responsive_height: Optional[ResponsiveOptions]
    padding: Optional[int]
    border_color: Optional[str]
    border_width: Optional[int]
    hover_color: Optional[str]


CORNER_POSSIBILITIES = ["right", "left", "top", "bottom"]


class BaseWidget(QWidget):
    DEFAULT_CORNER_RADIUS = 10
    DEFAULT_BORDER_WIDTH = 2
    DEFAULT_PADDING = 0

    def __init__(self, parent=None, settings: WidgetSettings = None, *args, **kwargs):
        super(BaseWidget, self).__init__(parent, *args, **kwargs)

        self._widget_id = ("widget-" + str(uuid.uuid4())).replace("-", "_")
        self.setObjectName(self._widget_id)

        self._apply_widget_flags()
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

        if 'corner' not in settings:
            self._settings.setdefault('corner', WidgetCorner(
                right=BaseWidget.DEFAULT_CORNER_RADIUS,
                left=BaseWidget.DEFAULT_CORNER_RADIUS,
                top=BaseWidget.DEFAULT_CORNER_RADIUS,
                bottom=BaseWidget.DEFAULT_CORNER_RADIUS
            ))

        for corner in CORNER_POSSIBILITIES:
            if corner not in self._settings["corner"]:
                self._settings.setdefault("corner", {
                    **self._settings["corner"],
                    corner: BaseWidget.DEFAULT_CORNER_RADIUS
                })

        if 'padding' not in self._settings:
            self._settings.setdefault('padding', BaseWidget.DEFAULT_PADDING)

        if 'border_color' not in self._settings:
            self._settings.setdefault('border_color', TailwindColors.slate.tw_slate_950)

        if 'border_width' not in self._settings:
            self._settings.setdefault('border_width', BaseWidget.DEFAULT_BORDER_WIDTH)

        if 'hover_color' not in self._settings:
            self._settings.setdefault('hover_color', TailwindColors.slate.tw_slate_300)

        style_sheet_string = self._get_style_sheet_string()
        self.setStyleSheet(style_sheet_string)
        self._apply_responsive()

    def _get_style_sheet_string(self):
        corner_radius = self._settings.get('corner', WidgetCorner(
            right=BaseWidget.DEFAULT_CORNER_RADIUS,
            left=BaseWidget.DEFAULT_CORNER_RADIUS,
            top=BaseWidget.DEFAULT_CORNER_RADIUS,
            bottom=BaseWidget.DEFAULT_CORNER_RADIUS,
        ))
        background_color = self._settings.get('background_color', TailwindColors.slate.tw_slate_50)
        padding = self._settings.get('padding', BaseWidget.DEFAULT_PADDING)
        border_width = self._settings.get('border_width', BaseWidget.DEFAULT_BORDER_WIDTH)
        border_color = self._settings.get('border_color', TailwindColors.slate.tw_slate_50)

        return f"""
            #{self._widget_id} {{
                background-color: {background_color};
                border-top-left-radius: {corner_radius['top']}px;
                border-top-right-radius: {corner_radius['right']}px;
                border-bottom-right-radius: {corner_radius['bottom']}px;
                border-bottom-left-radius: {corner_radius['left']}px;
                padding: {padding}px;
                border: {border_width}px solid {border_color};
            }}
            #{self._widget_id}:hover {{
                background-color: {self._settings['hover_color']};
            }}
        """

    def _apply_responsive(self):
        width_opt = self._settings.get('responsive_width', ResponsiveOptions.WIDTH_MATCH_PARENT)
        height_opt = self._settings.get('responsive_height', ResponsiveOptions.HEIGHT_MATCH_PARENT)

        horizontal = self._map_responsive_option(width_opt)
        vertical = self._map_responsive_option(height_opt)

        size_policy = QSizePolicy(horizontal, vertical)
        self.setSizePolicy(size_policy)

    @staticmethod
    def _map_responsive_option(opt: ResponsiveOptions) -> QSizePolicy.Policy:
        match opt:
            case ResponsiveOptions.WIDTH_MATCH_PARENT | ResponsiveOptions.HEIGHT_MATCH_PARENT:
                return QSizePolicy.Policy.Expanding
            case ResponsiveOptions.WIDTH_WRAP_CONTENT | ResponsiveOptions.HEIGHT_WRAP_CONTENT:
                return QSizePolicy.Policy.Minimum
            case ResponsiveOptions.SIZE_FILL_PARENT:
                return QSizePolicy.Policy.Expanding
            case ResponsiveOptions.SIZE_FILL_CONTENT:
                return QSizePolicy.Policy.Preferred
            case _:
                return QSizePolicy.Policy.Fixed

    def _apply_widget_flags(self):
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
