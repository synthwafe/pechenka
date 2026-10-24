import random
import shutil
from pathlib import Path

SRC = Path("labeled")   # куда экспортировали из X-AnyLabeling
DST = Path("dataset")
VAL_SHARE = 0.2
IMG_EXT = {".png", ".jpg", ".jpeg"}

random.seed(42)

# 1) Собираем все картинки
images = [p for p in SRC.rglob("*") if p.suffix.lower() in IMG_EXT]

# 2) Собираем метки по относительному пути (см. пункт "Коллизии имён")
labels = {p.relative_to(SRC).with_suffix(""): p
          for p in SRC.rglob("*.txt")
          if p.name != "classes.txt"}

random.shuffle(images)
n_val = max(1, int(len(images) * VAL_SHARE))

# 3) Создаём структуру папок один раз
for sub in ("images", "labels"):
    for split in ("train", "val"):
        (DST / sub / split).mkdir(parents=True, exist_ok=True)

for i, img in enumerate(images):
    split = "val" if i < n_val else "train"
    rel = img.relative_to(SRC)

    # копируем картинку, сохраняя подпапки (если они есть)
    dst_img = DST / "images" / split / rel
    dst_img.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(img, dst_img)

    # копируем метку, если она есть
    key = rel.with_suffix("")
    if key in labels:
        dst_lbl = DST / "labels" / split / key.with_suffix(".txt")
        dst_lbl.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(labels[key], dst_lbl)

with_labels = sum(1 for p in images if p.relative_to(SRC).with_suffix("") in labels)
print(f"Всего: {len(images)}, train: {len(images) - n_val}, val: {n_val}")
print(f"С разметкой: {with_labels}")