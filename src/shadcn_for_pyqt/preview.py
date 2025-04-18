import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from src.shadcn_for_pyqt.widgets.base import BaseWidget


class Preview(QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        super(Preview, self).__init__(parent, *args, **kwargs)

        self.setWindowTitle("Shadcn For PyQt Preview")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
    def add_widget(self, widget):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        self.layout.addWidget(widget, stretch=1)


class PreviewApplication(QApplication):
    def __init__(self, *args, **kwargs):
        super(PreviewApplication, self).__init__(*args, **kwargs)

        self._main_window: Preview | None = None

    def _setup_ui(self):
        self._main_window = Preview()

    def preview(self, widget=None):
        self._setup_ui()
        
        if widget:
            self._main_window.add_widget(widget)

        self._main_window.show()
        self.exec()


if __name__ == '__main__':
    app = PreviewApplication(sys.argv)

    test_widget = BaseWidget()
    app.preview(widget=test_widget)

    if not app:
        sys.exit(1)