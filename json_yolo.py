import json
import shutil
from pathlib import Path

SRC = Path("screenshots")   # где лежат картинки и .json из X-AnyLabeling
DST = Path("labeled")       # куда сложить результат для YOLO
DST.mkdir(exist_ok=True)

CLASSES = ["game"]
print("Классы: ", CLASSES)

done = 0
for i, js in enumerate(sorted(SRC.glob("*.json")), 1):
    data = json.loads(js.read_text(encoding="utf-8"))
    img = SRC / data["imagePath"]
    if not img.exists():
        print("Нет картинки для", js.name)
        continue

    W, H = data["imageWidth"], data["imageHeight"]
    lines = []
    for s in data["shapes"]:
        if s["label"] not in CLASSES:
            print(f"Пропущен класс '{s['label']}' в {js.name} (нет в classes.txt)")
            continue
        xs = [p[0] for p in s["points"]]
        ys = [p[1] for p in s["points"]]
        x1, x2 = max(0, min(xs)), min(W, max(xs))
        y1, y2 = max(0, min(ys)), min(H, max(ys))
        cls = CLASSES.index(s["label"])
        lines.append(f"{cls} {(x1 + x2) / 2 / W:.6f} {(y1 + y2) / 2 / H:.6f} "
                     f"{(x2 - x1) / W:.6f} {(y2 - y1) / H:.6f}")

    if not lines:
        continue
    name = f"img_{i:04d}"
    shutil.copy(img, DST / f"{name}{img.suffix.lower()}")
    (DST / f"{name}.txt").write_text("\n".join(lines), encoding="utf-8")
    done += 1

print(f"Готово: {done} картинок с разметкой в папке {DST}")