# camera_thread.py
import cv2
import time
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage
from core.yolo_engine import YOLOEngine


class CameraThread(QThread):
    frame_ready = Signal(QImage)
    count_ready = Signal(dict)  # kept for compatibility but will NOT be emitted in streaming

    def __init__(self, mode="detect", cam_index=0, target_fps=20):
        super().__init__()
        self.running = False
        self.mode = mode
        self.cam_index = cam_index
        self.yolo = None
        # Only initialize YOLO engine when needed (avoid heavy load if not used)
        try:
            # we still create an engine instance in case user wants to call process_static_frame_async
            self.yolo = YOLOEngine()
        except Exception as e:
            print("[CameraThread] YOLOEngine init failed:", e)
            self.yolo = None

        self.cap = None
        self.latest_frame_cv = None  # <-- WAJIB untuk Take Frame

        self._paused = False
        self.target_fps = target_fps
        self._frame_interval = 1.0 / float(self.target_fps) if self.target_fps > 0 else 0.05

    def run(self):
        self.running = True
        self.cap = cv2.VideoCapture(self.cam_index, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            print(f"[CameraThread] Gagal membuka kamera index={self.cam_index}")
            self.running = False
            return

        last_time = 0.0
        while self.running:
            now = time.time()
            if now - last_time < self._frame_interval:
                time.sleep(max(0.0, self._frame_interval - (now - last_time)))
            last_time = time.time()

            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.01)
                continue

            # SIMPAN FRAME TERAKHIR (WAJIB)
            self.latest_frame_cv = frame.copy()

            # Jika sedang pause (freeze), jangan kirim update ke UI (tampilan dibekukan)
            if self._paused:
                # still keep latest_frame_cv up-to-date but do not emit frame
                continue

            # Jika mode detect dan developer ingin overlay, kita bisa menjalankan YOLO
            # Namun untuk "count" mode (UI Counter) kita **tidak** menjalankan YOLO di streaming
            if self.mode == "detect":
                # run YOLO and draw boxes for display-only
                if self.yolo is not None:
                    try:
                        results = self.yolo.detect(frame)
                        for r in results:
                            for box in r.boxes:
                                cls = int(box.cls)
                                label = self.yolo.names[cls] if hasattr(self.yolo, "names") else str(cls)
                                x1, y1, x2, y2 = box.xyxy[0]
                                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                                cv2.putText(frame, label, (int(x1), int(y1) - 5),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    except Exception as e:
                        print("[CameraThread] YOLO detect error in streaming:", e)

            # convert and emit frame for UI
            try:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
                self.frame_ready.emit(img)
            except Exception as e:
                # if conversion fails, skip this frame
                print("[CameraThread] frame conversion error:", e)
                continue

        # cleanup
        try:
            if self.cap is not None and self.cap.isOpened():
                self.cap.release()
        except Exception:
            pass

    def stop(self):
        # signal stop, then wait for thread to finish
        self.running = False
        self.resume()  # ensure not paused so loop can exit
        self.quit()
        self.wait(2000)

        try:
            if self.cap is not None and self.cap.isOpened():
                self.cap.release()
        except Exception:
            pass

    def pause(self):
        """Pause emitting frames (freeze display). Camera keeps grabbing frames internally."""
        self._paused = True

    def resume(self):
        """Resume emitting frames."""
        self._paused = False

    def process_static_frame_async(self, frame):
        """
        Deprecated: kept for compatibility.
        Prefer using StaticProcessThread for heavy YOLO processing.
        """
        if self.yolo is None:
            return {}

        try:
            results = self.yolo.detect(frame)
            count_dict = {}
            for r in results:
                for box in r.boxes:
                    label = self.yolo.names[int(box.cls)]
                    count_dict[label] = count_dict.get(label, 0) + 1
            # Optional: emit count (but be careful in UI – usually you don't want this)
            self.count_ready.emit(count_dict)
            return count_dict
        except Exception as e:
            print("[CameraThread] process_static_frame_async error:", e)
            return {}
