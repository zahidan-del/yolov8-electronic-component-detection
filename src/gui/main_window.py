from PySide6.QtWidgets import QTabWidget
from gui.tab_detection import DetectionTab
from gui.tab_counter import CounterTab

class MainWindow(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Electronic Component Vision (YOLOv8)")
        self.setMinimumSize(900, 600)

        # Tab mode deteksi
        self.tab_detection = DetectionTab()
        self.addTab(self.tab_detection, "Realtime Detection")

        # Tab mode hitung komponen
        self.tab_counter = CounterTab()
        self.addTab(self.tab_counter, "Component Counter")
