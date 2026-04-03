# core/static_process_thread.py
from PySide6.QtCore import QThread, Signal
# Asumsi: YOLOEngine berisi logika pemuatan model dan metode detect()
from core.yolo_engine import YOLOEngine 
import cv2 

class StaticProcessThread(QThread):
    """
    Thread untuk menjalankan YOLO pada frame statis (satu kali).
    Mengirimkan hasil count (dict) dan frame BGR yang sudah digambar 
    (numpy array) via signal `result_ready`.
    """
    # Signal sekarang mengirim dua argumen: dict untuk count, object untuk frame (numpy array)
    result_ready = Signal(dict, object) 

    def __init__(self, frame_bgr):
        super().__init__()
        # Salin frame untuk memastikan thread aman (thread-safe)
        self.frame = frame_bgr.copy() if frame_bgr is not None else None
        self.yolo = None

    def run(self):
        # 1. Cek Frame Kosong
        if self.frame is None:
            # Emit dua nilai: dict kosong dan None (untuk frame)
            self.result_ready.emit({}, None) 
            return

        try:
            # 2. Inisialisasi YOLO Engine (Lazy Loading)
            if self.yolo is None:
                self.yolo = YOLOEngine()

            # 3. Deteksi YOLO
            results = self.yolo.detect(self.frame)
            count_dict = {}
            
            # Buat salinan frame untuk digambar (agar frame asli tetap utuh)
            frame_with_box = self.frame.copy()

            # 4. Proses Hasil dan Hitung Objek (Count)
            for r in results:
                for box in r.boxes:
                    cls = int(box.cls)
                    # Ambil label atau gunakan ID kelas jika nama tidak tersedia
                    label = self.yolo.names[cls] if hasattr(self.yolo, "names") else str(cls)
                    
                    # Logika Counting
                    count_dict[label] = count_dict.get(label, 0) + 1
                    
                    # 5. Gambar Bounding Box (untuk display di UI)
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy() # Pastikan koordinat diambil dengan benar
                    
                    # Gambar kotak (warna hijau)
                    cv2.rectangle(frame_with_box, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    
                    # Gambar teks label
                    cv2.putText(frame_with_box, 
                                f"{label}", 
                                (int(x1), int(y1) - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # 6. Kirim Hasil
            # Emit count_dict (dict) dan frame_with_box (numpy array)
            self.result_ready.emit(count_dict, frame_with_box) 
            
        except Exception as e:
            print("[StaticProcessThread] Error during static YOLO processing:", e)
            # Kirim hasil kosong jika terjadi error
            self.result_ready.emit({}, self.frame.copy() if self.frame is not None else None)