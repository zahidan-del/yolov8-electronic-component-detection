from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QComboBox,
    QMessageBox, QApplication
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import cv2

from core.camera_thread import CameraThread


def list_available_cameras(max_test=10):
    """Scan kamera yang tersedia"""
    cams = []
    for i in range(max_test):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            cams.append(i)
        cap.release()
    return cams


class DetectionTab(QWidget):
    def __init__(self):
        super().__init__()


        # -------------------- TITLE --------------------
        self.title = QLabel("Electronic Component Detection", self)
        self.title.setGeometry(150, 10, 600, 30)  # atur posisi dan ukuran
        self.title.setStyleSheet("color: #1E90FF; font-size: 25px; font-weight: bold;")
        self.title.setAlignment(Qt.AlignCenter)

        # -------------------- CAMERA FEED --------------------
        self.label = QLabel("Camera Feed", self)
        self.label.setGeometry(20, 60, 640, 480)  # posisi kiri
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: black; color: white;")
        self.reset_camera_label()

        # -------------------- BUTTONS --------------------
        # Start Button
        self.btn_start = QPushButton("Start Detection", self)
        self.btn_start.setGeometry(705, 65, 150, 40)
        self.btn_start.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:disabled {
                background-color: #75b3f0;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)

        # Stop Button
        self.btn_stop = QPushButton("Stop", self)
        self.btn_stop.setGeometry(705, 115, 150, 40)
        self.btn_stop.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:disabled {
                background-color: #75b3f0;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.btn_stop.setEnabled(False)

        # Scan Camera Button
        self.btn_scan = QPushButton("Scan Camera", self)
        self.btn_scan.setGeometry(705, 165, 150, 40)
        self.btn_scan.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:disabled {
                background-color: #75b3f0;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)

        # Camera Dropdown
        self.camera_box = QComboBox(self)
        self.camera_box.setGeometry(705, 215, 150, 40)
        self.camera_box.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:disabled {
                background-color: #75b3f0;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.camera_box.currentIndexChanged.connect(self.change_camera)

        # Scan awal
        self.refresh_camera_list(first_time=True)

        # -------------------- CAMERA THREAD --------------------
        default_cam = self.camera_box.itemData(self.camera_box.currentIndex())
        self.cam_thread = CameraThread(mode="detect", cam_index=default_cam)
        self.cam_thread.frame_ready.connect(self.update_frame)

        # -------------------- SIGNALS --------------------
        self.btn_start.clicked.connect(self.start_cam)
        self.btn_stop.clicked.connect(self.stop_cam)
        self.btn_scan.clicked.connect(self.scan_cameras)

    # ======================================================
    def reset_camera_label(self):
        """Set frame hitam default"""
        self.label.clear()
        self.label.setStyleSheet("background-color: black; color: white;")
        self.label.setText("Camera Feed")

    # ======================================================
    def start_cam(self):
        if not self.cam_thread.isRunning():
            self.cam_thread.running = True
            self.cam_thread.start()
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)

    # ======================================================
    def stop_cam(self):
        try:
            if self.cam_thread.isRunning():
                self.cam_thread.stop()

            # Reset frame ke hitam
            self.reset_camera_label()

            self.btn_start.setEnabled(True)
            self.btn_stop.setEnabled(False)

        except Exception as e:
            print("Error saat stop camera:", e)

    # ======================================================
    def change_camera(self, index):
        cam_index = self.camera_box.itemData(index)
        if cam_index is not None:
            if self.cam_thread.isRunning():
                self.cam_thread.stop()
            self.cam_thread.cam_index = cam_index

    # ======================================================
    def update_frame(self, img):
        self.label.setPixmap(QPixmap.fromImage(img))

    # ======================================================
    def scan_cameras(self):
        """Scan kamera dengan loading"""
        self.label.setText("Scanning Cameras...")
        self.label.setStyleSheet("background-color: gray; color: white;")
        QApplication.processEvents()  # refresh GUI

        self.refresh_camera_list(first_time=False)

    # ======================================================
    def refresh_camera_list(self, first_time=False):
        previous_cam = self.camera_box.currentData()

        available_cams = list_available_cameras()
        self.camera_box.clear()

        # Tambahkan kamera yang tersedia
        for cam_id in available_cams:
            self.camera_box.addItem(f"Camera {cam_id}", cam_id)

        # Tidak ada kamera
        if not available_cams:
            self.btn_start.setEnabled(False)
            QMessageBox.warning(self, "No Cameras Detected",
                                "Tidak ada kamera yang terdeteksi oleh sistem.")
            self.reset_camera_label()
            return

        # Kamera tersedia → enable Start
        self.btn_start.setEnabled(True)

        # Jika bukan startup → cek kamera sebelumnya
        if not first_time:
            if previous_cam not in available_cams:
                QMessageBox.warning(
                    self,
                    "Camera Removed",
                    f"Kamera sebelumnya (Camera {previous_cam}) tidak ditemukan.\n"
                    f"Silakan pilih kamera lain."
                )
            else:
                index = self.camera_box.findData(previous_cam)
                if index >= 0:
                    self.camera_box.setCurrentIndex(index)

        # Restore frame ke hitam
        self.reset_camera_label()
        print("Camera list updated:", available_cams)
