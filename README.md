# YOLOv8 Electronic Component Detection

**A realtime electronic component detection and counting system using YOLOv8 with a PyQt5-based GUI.**



---

## About the Project

This project is the final assignment for the **Computer Vision Practicum** course, aimed at building an automatic electronic component classification system using a camera. The system is capable of detecting and counting electronic components in **realtime** without manual identification.

### Background

The process of identifying electronic components such as resistors, capacitors, transistors, and ICs is often done manually, requiring high precision and potentially leading to errors. This system was developed as a solution to improve efficiency and accuracy in electronics learning and practicum activities.

---

## Features

- Realtime Detection — Detect components directly through a camera feed
- Component Counter — Count the number of each component from a camera snapshot
- PyQt5 GUI — Easy-to-use interface with 2 tabs (Realtime & Counter)
- Bounding Box — Detection visualization with colored bounding boxes
- Multi-Camera Support — Supports selection of connected cameras

---

## Detectable Components

| No | Component  | Number of Instances |
|----|------------|---------------------|
| 1  | Capacitor  | 2,803               |
| 2  | IC         | 2,783               |
| 3  | LED        | 2,791               |
| 4  | Resistor   | 2,774               |
| 5  | Transistor | 2,856               |

---

## Demo Video

[Click here to watch the application demo](https://drive.google.com/file/d/1H69XXpEX6p_C0FJvo_hS6dOoXpTJWQel/view?usp=sharing)



---

### Dataset Details

| Description        | Amount            |
|--------------------|-------------------|
| Total Images       | 795               |
| Training Set       | 597 images        |
| Validation Set     | 132 images        |
| Testing Set        | 66 images         |
| After Augmentation | 1,989 images (3x) |
| Number of Classes  | 5                 |

### Preprocessing and Augmentation (Roboflow)

- Flip: Horizontal and Vertical
- Rotation: Between -15 and +15 degrees
- Saturation: Between -25% and +25%
- Image Size: 640x640

---

## Model Results

The model was trained using **YOLOv8** with **200 epochs** and an image size of **640x640**.

### Performance Per Class (mAP@0.5)

| Class           | Precision | mAP@0.5  |
|-----------------|-----------|----------|
| Capacitor       | 0.98      | 0.950    |
| IC              | 0.95      | 0.949    |
| LED             | 0.89      | 0.847    |
| Resistor        | 0.69      | 0.549    |
| Transistor      | 0.98      | 0.951    |
| **All Classes** | -         | **0.849**|

### Metrics Summary

- mAP@0.5 (all classes): 0.849
- Recall (all classes): 0.96
- F1-Score (all classes): 0.83 at confidence 0.337
- Precision (all classes): 1.00 at confidence 0.967

---

## Folder Structure

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

## Installation

### Prerequisites

- Python 3.8+
- Webcam / USB Camera

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/zahidan-del/yolov8-electronic-component-detection.git
cd yolov8-electronic-component-detection

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download the best.pt model
# Download from Releases and place it in the models/ folder
```

---

## How to Use

```bash
python src/main.py
```

### Tab 1 - Realtime Detection

1. Select a camera from the dropdown
2. Click Start Detection to begin realtime detection
3. Click Stop to halt detection

### Tab 2 - Component Counter

1. Select a camera from the dropdown
2. Click Start Camera Feed to turn on the camera
3. Click Take Frame to capture a snapshot
4. Click Count Components to count the detected components

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

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## References

1. I. Atik, "Classification of Electronic Components Based on Convolutional Neural Network Architecture," Energies, vol. 15, no. 7, 2022.
2. S. Hozyn, "Convolutional Neural Networks for Classifying Electronic Components," Energies, vol. 16, no. 2, 2023.
3. P. Chand and S. Lal, "Vision-Based Detection and Classification of Used Electronic Parts," Sensors, vol. 22, no. 23, 2022.
4. L. Zhou and L. Zhang, "A Novel Convolutional Neural Network for Electronic Component Classification with Diverse Backgrounds," Int. J. Model. Simul. Sci. Comput., 2021.
5. E. Soylu and I. Kaya, "Classification of Electronics Components using Deep Learning," Sakarya Univ. J. Comput. Inf. Sci., vol. 7, no. 1, pp. 36-45, 2024.

---



