# Демонстрация работы проекта: окно показывает, что видит нейросеть,
# и одновременно кликает по найденной печеньке.
# Запуск: python demo.py
# Выход: клавиша Q в окне просмотра или мышь в левый верхний угол экрана.
import time
from pathlib import Path

import cv2
import numpy as np
import pyautogui
from ultralytics import YOLO

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

MODEL = Path("runs/detect/cookie_detector/weights/best.pt")
if not MODEL.exists():          # скачано с GitHub: best.pt лежит рядом со скриптом
    MODEL = Path(__file__).with_name("best.pt")
model = YOLO(str(MODEL))
CLICK = True        # False - только показывать рамки, без кликов
CONF = 0.7

clicks = 0
print("Старт через 3 с. Выход: Q в окне просмотра или мышь в левый верхний угол.")
time.sleep(3)

try:
    while True:
        frame = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
        result = model(frame, conf=CONF, verbose=False)[0]

        if CLICK and len(result.boxes):
            sw, sh = pyautogui.size()
            kx, ky = sw / frame.shape[1], sh / frame.shape[0]
            best = result.boxes[int(result.boxes.conf.argmax())]
            x1, y1, x2, y2 = best.xyxy[0].tolist()
            for _ in range(5):
                pyautogui.click((x1 + x2) / 2 * kx, (y1 + y2) / 2 * ky)
            clicks += 5

        view = result.plot()                                  # рамки + уверенность
        cv2.putText(view, f"Clicks: {clicks}", (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 255), 4)
        view = cv2.resize(view, None, fx=0.4, fy=0.4)
        cv2.imshow("YOLO demo (Q - exit)", view)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
except pyautogui.FailSafeException:
    pass

cv2.destroyAllWindows()
print(f"Остановлено. Всего кликов: {clicks}")
