# Задача 3. Обучение модели YOLO.
# Запуск: python train.py
# Результат: runs/detect/cookie_detector/weights/best.pt
from ultralytics import YOLO

if __name__ == "__main__":   # на Windows без этой строки обучение падает
    model = YOLO("yolov8n.pt")  # предобученная модель, скачается сама
    model.train(
        data="data.yaml",
        epochs=100,          # на слабом ПК без видеокарты можно 50
        imgsz=640,
        batch=16,            # при нехватке памяти уменьшите до 8 или 4
        workers=0,           # на Windows многопоточная загрузка часто ломается
        name="cookie_detector",
        exist_ok=True,       # не создавать cookie_detector2, 3, ...
        patience=50,         # остановка, если 50 эпох нет улучшений
    )
