from ultralytics import YOLO

class YOLOEngine:
    def __init__(self, model_path="models/bestV6.pt"):
        self.model = YOLO(model_path)
        self.names = self.model.names

    def detect(self, frame):
        return self.model(frame, stream=True)
