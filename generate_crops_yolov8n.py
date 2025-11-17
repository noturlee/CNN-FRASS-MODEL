import os
import cv2
from ultralytics import YOLO
from tqdm import tqdm



RAW_DATA_DIR = "archive-3"          
OUTPUT_DIR = "DatasetB/crops_v2"     
MODEL = YOLO("yolov8n.pt")

CONF_THRESHOLD = 0.25

YOLO_INPUT_SIZE = 960   

VALID_EXT = (".jpg", ".jpeg", ".png")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def collect_images(root):
    paths = []
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.lower().endswith(VALID_EXT):
                paths.append(os.path.join(dirpath, f))
    return paths

all_images = collect_images(RAW_DATA_DIR)
print(f"Found {len(all_images)} raw images to process")



crop_count = 0

for img_path in tqdm(all_images, desc="Extracting crops"):
    try:
        img = cv2.imread(img_path)
        if img is None:
            continue

        if img.mean() < 10:
            continue

        h, w = img.shape[:2]
        scale = YOLO_INPUT_SIZE / max(h, w)
        resized = cv2.resize(img, (int(w * scale), int(h * scale)))

        results = MODEL(resized, conf=CONF_THRESHOLD, verbose=False)

        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()

            for box in boxes:
                x1, y1, x2, y2 = box.astype(int)

                pad = 8
                x1 = max(x1 - pad, 0)
                y1 = max(y1 - pad, 0)
                x2 = min(x2 + pad, resized.shape[1])
                y2 = min(y2 + pad, resized.shape[0])

                crop = resized[y1:y2, x1:x2]
                if crop.size == 0:
                    continue

                if crop.shape[0] < 50 or crop.shape[1] < 50:
                    continue
                if crop.mean() < 20:
                    continue

                # save crop
                crop_path = os.path.join(OUTPUT_DIR, f"crop_{crop_count}.jpg")
                cv2.imwrite(crop_path, crop)
                crop_count += 1

    except Exception as e:
        print("Error:", img_path, e)

print(f"\nDONE! Saved {crop_count} crops into {OUTPUT_DIR}")
print("Goal: 400+ — If lower, we will run with even more sensitive settings.")
