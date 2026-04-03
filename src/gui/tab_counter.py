# tab_counter.py
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QComboBox,
    QMessageBox, QTableWidget, QTableWidgetItem, QApplication
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

import cv2

from core.camera_thread import CameraThread
from core.static_process_thread import StaticProcessThread


def cv2_to_qpixmap(frame_bgr):
    try:
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        return QPixmap.fromImage(QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888))
    except Exception:
        return None


class CounterTab(QWidget):
    def __init__(self):
        super().__init__()
        self.cam_thread = None
        self.captured_frame_cv = None
        self.worker = None

        # ===================== UI =====================
        self.title = QLabel("Electronic Component Counter", self)
        self.title.setGeometry(150, 10, 600, 30)
        self.title.setStyleSheet("color: #1E90FF; font-size: 25px; font-weight: bold;")
        self.title.setAlignment(Qt.AlignCenter)

        self.label = QLabel("Camera Feed", self)
        self.label.setGeometry(20, 60, 640, 480)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: black; color: white;")
        self.reset_camera_label()

        # status label (pisah dari label gambar)
        self.status = QLabel("", self)
        self.status.setGeometry(20, 545, 640, 25)
        self.status.setAlignment(Qt.AlignLeft)

        self.btn_start = QPushButton("Start Camera Feed", self)
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

        self.btn_stop = QPushButton("Stop Camera Feed", self)
        self.btn_stop.setGeometry(705, 115, 150, 40)
        self.btn_stop.setEnabled(False)
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

        self.btn_take_frame = QPushButton("Take Frame", self)
        self.btn_take_frame.setGeometry(705, 275, 150, 40)
        self.btn_take_frame.setEnabled(False)
        self.btn_take_frame.setStyleSheet("""
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

        self.btn_count = QPushButton("Count Components", self)
        self.btn_count.setGeometry(705, 325, 150, 40)
        self.btn_count.setEnabled(False)
        self.btn_count.setStyleSheet("""
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

        self.table = QTableWidget(self)
        self.table.setGeometry(680, 370, 300, 170)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Component", "Count"])
        

        # scan kamera awal
        self.scan_cameras()

        # event
        self.btn_start.clicked.connect(self.start_cam)
        self.btn_stop.clicked.connect(self.stop_cam)
        self.btn_scan.clicked.connect(self.scan_cameras)
        self.camera_box.currentIndexChanged.connect(self.change_camera)
        self.btn_take_frame.clicked.connect(self.take_frame)
        self.btn_count.clicked.connect(self.count_frame)

    # ======================================================
    def scan_camera_list(self, is_loading=False): # Tambahkan argumen is_loading
        self.camera_box.clear()
        
        # Logika pemindaian kamera
        available_cams = []
        for i in range(10):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened():
                available_cams.append(i)
                self.camera_box.addItem(f"Camera {i}", i)
            cap.release()

        # setup camera thread for selected camera but do not start
        if self.camera_box.count() > 0:
            self.setup_camera_thread(self.camera_box.currentData())
        
        # Tambahkan notifikasi jika tidak ada kamera, mirip DetectionTab
        if not available_cams and not is_loading:
            QMessageBox.warning(self, "No Cameras Detected",
                                 "Tidak ada kamera yang terdeteksi oleh sistem.")

    def scan_cameras(self):
        """Scan kamera dengan loading"""
        # Tampilkan pesan loading
        self.label.setText("Scanning Cameras...")
        self.label.setStyleSheet("background-color: gray; color: white;")
        QApplication.processEvents()  # refresh GUI agar loading muncul

        # Panggil logika pemindaian yang sebenarnya
        self.scan_camera_list(is_loading=True)

        # Kembalikan tampilan label ke default setelah selesai
        self.reset_camera_label()

    # ======================================================
    def setup_camera_thread(self, cam_index):
        # stop existing thread safely
        if self.cam_thread:
            try:
                self.cam_thread.stop()
            except Exception:
                pass

        # Create camera thread: in mode "count" thread will only emit frames (no YOLO)
        self.cam_thread = CameraThread(mode="count", cam_index=cam_index)
        self.cam_thread.frame_ready.connect(self._on_frame_ready)
        # camera_thread will NOT emit count_ready during streaming (we keep signal but it won't be used)
        # self.cam_thread.count_ready.connect(self._on_count_ready)  # intentionally not connected

    # ======================================================
    def start_cam(self):
        if not self.cam_thread:
            QMessageBox.warning(self, "Camera", "Tidak ada kamera yang terdeteksi.")
            return

        self.cam_thread.start()
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.camera_box.setEnabled(False)
        self.btn_take_frame.setEnabled(True)
        self.table.setRowCount(0)
        self.status.setText("Camera started.")

    def stop_cam(self):
        if self.cam_thread:
            self.cam_thread.resume()  # make sure not paused
            self.cam_thread.stop()
            self.cam_thread.wait(50)

        self.label.clear()       # <- tambahkan
        self.reset_camera_label()

        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.camera_box.setEnabled(True)
        self.btn_take_frame.setEnabled(False)
        self.btn_count.setEnabled(False)
        self.status.setText("Camera stopped.")
        self.table.setRowCount(0)

    # ======================================================
    def change_camera(self, idx):
        cam_index = self.camera_box.itemData(idx)
        if cam_index is not None:
            self.setup_camera_thread(cam_index)

    def reset_camera_label(self):
        """Set frame hitam default"""
        self.label.clear()
        self.label.setStyleSheet("background-color: black; color: white;")
        self.label.setText("Camera Feed")

    # ======================================================
    def _on_frame_ready(self, qimage):
        # Only update display if not frozen (CameraThread handles freeze by pause())
        pix = QPixmap.fromImage(qimage).scaled(self.label.size(), Qt.KeepAspectRatio)
        self.label.setPixmap(pix)

    def _on_count_ready(self, count_dict):
        # This slot remains if someday you want to connect streaming counts.
        self.table.setRowCount(len(count_dict))
        for row, (k, v) in enumerate(count_dict.items()):
            self.table.setItem(row, 0, QTableWidgetItem(k))
            self.table.setItem(row, 1, QTableWidgetItem(str(v)))

    # ======================================================
    def take_frame(self):
        if not self.cam_thread:
            QMessageBox.warning(self, "Camera", "Camera thread belum siap.")
            return

        frame = self.cam_thread.latest_frame_cv

        if frame is None:
            QMessageBox.warning(self, "Frame Error", "Frame belum tersedia.")
            return

        # Pause camera thread emission (freeze UI) but keep thread running
        self.cam_thread.pause()
        self.captured_frame_cv = frame.copy()

        pix = cv2_to_qpixmap(self.captured_frame_cv)
        if pix:
            self.label.setPixmap(pix.scaled(self.label.size(), Qt.KeepAspectRatio))

        self.btn_count.setEnabled(True)
        self.status.setText("Frame taken and frozen. Ready to count.")

    # ======================================================
    def count_frame(self):
        if self.captured_frame_cv is None:
            QMessageBox.warning(self, "No Frame", "Ambil frame dahulu.")
            return

        self.status.setText("Processing frame...")
        self.btn_count.setEnabled(False)

        # jalankan YOLO di background thread (statik)
        # pastikan tidak ada worker aktif
        if self.worker is not None and self.worker.isRunning():
            QMessageBox.information(self, "Busy", "Proses sebelumnya belum selesai.")
            return

        self.worker = StaticProcessThread(self.captured_frame_cv)
        self.worker.result_ready.connect(self._on_static_done)
        self.worker.start()

    def _on_static_done(self, count_dict, processed_frame):
        # tampilkan bounding box di QLabel
        pix = cv2_to_qpixmap(processed_frame)
        if pix:
            self.label.setPixmap(pix.scaled(self.label.size(), Qt.KeepAspectRatio))

        # update table
        self.table.setRowCount(len(count_dict))
        for row, (k, v) in enumerate(count_dict.items()):
            self.table.setItem(row, 0, QTableWidgetItem(k))
            self.table.setItem(row, 1, QTableWidgetItem(str(v)))

        self.status.setText("Frame processed with bounding box.")

        # kamera kembali jalan (user bisa ambil frame lagi)
        #if self.cam_thread:
            #self.cam_thread.resume()

        self.btn_count.setEnabled(True)


    # ======================================================
    def closeEvent(self, event):
        # Make sure threads are stopped when widget closed
        try:
            if self.worker is not None and self.worker.isRunning():
                self.worker.terminate()
                self.worker.wait(200)
        except Exception:
            pass

        try:
            if self.cam_thread:
                self.cam_thread.stop()
        except Exception:
            pass

        event.accept()
