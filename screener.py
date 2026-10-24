import os
import time
from datetime import datetime
import pyautogui

SAVE_DIR = "screenshots"
INTERVAL = 3   # секунд между снимками
MAX_SHOTS = 100  # 0 — без ограничения

os.makedirs(SAVE_DIR, exist_ok=True)
print(f"Снимок каждые {INTERVAL} с. Остановка: Ctrl+C")
time.sleep(3)  # время переключиться на окно игры

count = 0
try:
    while MAX_SHOTS == 0 or count < MAX_SHOTS:
        name = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        pyautogui.screenshot().save(f"{SAVE_DIR}/shot_{name}.png")
        count += 1
        print(f"[{count}] сохранено")
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    pass

print(f"Остановлено. Всего скриншотов: {count}")