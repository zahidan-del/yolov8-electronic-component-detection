# YOLOv8 Electronic Component Detection
**Sistem deteksi dan penghitungan komponen elektronik secara realtime menggunakan YOLOv8 dengan antarmuka GUI berbasis PyQt5.**
## Tentang Project

Project ini merupakan tugas akhir mata kuliah **Praktik Computer Vision** yang bertujuan membangun sistem klasifikasi komponen elektronik secara otomatis menggunakan kamera. Sistem ini mampu mendeteksi dan menghitung komponen elektronik secara **realtime** tanpa perlu identifikasi manual.

### Latar Belakang

Proses identifikasi komponen elektronik seperti resistor, kapasitor, transistor, dan IC sering kali dilakukan secara manual yang memerlukan ketelitian tinggi dan berpotensi menimbulkan kesalahan. Sistem ini hadir sebagai solusi untuk meningkatkan efisiensi dan akurasi dalam proses pembelajaran maupun praktikum elektronika.

---

## Fitur

- Realtime Detection — Deteksi komponen secara langsung melalui kamera
- Component Counter — Menghitung jumlah setiap komponen dari snapshot kamera
- GUI PyQt5 — Antarmuka yang mudah digunakan dengan 2 tab (Realtime & Counter)
- Bounding Box — Visualisasi deteksi dengan kotak pembatas berwarna
- Multi-Camera Support — Mendukung pemilihan kamera yang terhubung

---

## Komponen yang Dapat Dideteksi

| No | Komponen   | Jumlah Instance |
|----|------------|----------------|
| 1  | Capacitor  | 2.803          |
| 2  | IC         | 2.783          |
| 3  | LED        | 2.791          |
| 4  | Resistor   | 2.774          |
| 5  | Transistor | 2.856          |

---

## Demo Video

[Klik disini untuk melihat demo aplikasi](https://drive.google.com/file/d/1H69XXpEX6p_C0FJvo_hS6dOoXpTJWQel/view?usp=sharing)


## Dataset

Dataset dikumpulkan secara mandiri menggunakan kamera dan dipreprocessing menggunakan **Roboflow**.

**Download Dataset:** [Google Drive](https://drive.google.com/your-dataset-link) *(ganti dengan link dataset kamu)*

### Detail Dataset

| Keterangan         | Jumlah            |
|--------------------|-------------------|
| Total Gambar       | 795               |
| Training Set       | 597 gambar        |
| Validation Set     | 132 gambar        |
| Testing Set        | 66 gambar         |
| Setelah Augmentasi | 1.989 gambar (3x) |
| Jumlah Kelas       | 5                 |

### Preprocessing dan Augmentasi (Roboflow)

- Flip: Horizontal and Vertical
- Rotation: Between -15 and +15 degree
- Saturation: Between -25% and +25%
- Image Size: 640x640

---

## Hasil Model

Model dilatih menggunakan **YOLOv8** dengan **200 epoch** dan ukuran gambar **640x640**.

### Performa Per Kelas (mAP@0.5)

| Kelas           | Precision | mAP@0.5  |
|-----------------|-----------|----------|
| Capacitor       | 0.98      | 0.950    |
| IC              | 0.95      | 0.949    |
| LED             | 0.89      | 0.847    |
| Resistor        | 0.69      | 0.549    |
| Transistor      | 0.98      | 0.951    |
| **All Classes** | -         | **0.849**|

### Ringkasan Metrik

- mAP@0.5 (all classes): 0.849
- Recall (all classes): 0.96
- F1-Score (all classes): 0.83 at confidence 0.337
- Precision (all classes): 1.00 at confidence 0.967

---

## Struktur Folder

```
yolov8-electronic-component-detection/
|
|-- README.md
|-- requirements.txt
|-- .gitignore
|
|-- src/
|   |-- main.py
|   |-- gui.py
|   └-- detector.py
|
|-- models/
|   └-- README.md
|
|-- training/
|   └-- train.py
|
└-- assets/
    |-- screenshot1.png
    └-- screenshot2.png
```

---

## Instalasi

### Prasyarat

- Python 3.8+
- Webcam / Kamera USB

### Langkah Instalasi

```bash
# 1. Clone repository
git clone https://github.com/zahidan-del/yolov8-electronic-component-detection.git
cd yolov8-electronic-component-detection

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download model best.pt
# Download dari Releases lalu letakkan di folder models/
```

---

## Cara Penggunaan

```bash
python src/main.py
```

### Tab 1 - Realtime Detection

1. Pilih kamera dari dropdown
2. Klik Start Detection untuk memulai deteksi realtime
3. Klik Stop untuk menghentikan

### Tab 2 - Component Counter

1. Pilih kamera dari dropdown
2. Klik Start Camera Feed untuk menyalakan kamera
3. Klik Take Frame untuk mengambil snapshot
4. Klik Count Components untuk menghitung komponen

---

## Requirements

```
ultralytics
opencv-python
PyQt5
torch
torchvision
numpy
```

Install semua dengan:

```bash
pip install -r requirements.txt
```



---

## Referensi

1. I. Atik, "Classification of Electronic Components Based on Convolutional Neural Network Architecture," Energies, vol. 15, no. 7, 2022.
2. S. Hozyn, "Convolutional Neural Networks for Classifying Electronic Components," Energies, vol. 16, no. 2, 2023.
3. P. Chand and S. Lal, "Vision-Based Detection and Classification of Used Electronic Parts," Sensors, vol. 22, no. 23, 2022.
4. L. Zhou and L. Zhang, "A Novel Convolutional Neural Network for Electronic Component Classification with Diverse Backgrounds," Int. J. Model. Simul. Sci. Comput., 2021.
5. E. Soylu and I. Kaya, "Classification of Electronics Components using Deep Learning," Sakarya Univ. J. Comput. Inf. Sci., vol. 7, no. 1, pp. 36-45, 2024.

---

