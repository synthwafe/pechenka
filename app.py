# Задача 4. Автокликер: находит печеньку на экране и кликает по ней.
# Запуск: python app.py, затем за 3 секунды переключиться на игру.
# Остановка: Ctrl+C в терминале или мышь в левый верхний угол экрана.
import time
from pathlib import Path

import cv2
import numpy as np
import pyautogui
from ultralytics import YOLO

pyautogui.FAILSAFE = True   # мышь в левый верхний угол — аварийная остановка
pyautogui.PAUSE = 0

MODEL = Path("runs/detect/cookie_detector/weights/best.pt")
if not MODEL.exists():          # скачано с GitHub: best.pt лежит рядом со скриптом
    MODEL = Path(__file__).with_name("best.pt")
model = YOLO(str(MODEL))
CONF = 0.7                  # порог уверенности


def grab():
    """Скриншот + коэффициенты пересчёта (на случай масштаба 125%/150%)."""
    frame = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    sw, sh = pyautogui.size()
    return frame, sw / frame.shape[1], sh / frame.shape[0]


def find_and_click():
    frame, kx, ky = grab()
    boxes = model(frame, conf=CONF, verbose=False)[0].boxes
    if len(boxes) == 0:
        return False
    best = boxes[int(boxes.conf.argmax())]
    x1, y1, x2, y2 = best.xyxy[0].tolist()
    cx, cy = (x1 + x2) / 2 * kx, (y1 + y2) / 2 * ky
    for _ in range(10):             # 10 кликов за секунду
        pyautogui.click(cx, cy)
        time.sleep(0.1)
    print(f"Клик: ({cx:.0f}, {cy:.0f}), уверенность {float(best.conf):.2f}")
    return True


print("Старт через 3 с. Остановка: Ctrl+C или мышь в левый верхний угол.")
time.sleep(3)
try:
    while True:
        time.sleep(1 if find_and_click() else 0.5)
except (KeyboardInterrupt, pyautogui.FailSafeException):
    print("Остановлено")
