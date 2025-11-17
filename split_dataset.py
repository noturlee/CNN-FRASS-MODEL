import os
import shutil
import random

SOURCE_DIR = "DatasetB"
TARGET_DIR = "DatasetB_split"

CLASSES = ["Healthy", "Diseased", "Pests"]

TRAIN_RATIO = 0.6
VAL_RATIO = 0.2
TEST_RATIO = 0.2

random.seed(42)

# create target directory structure
for subset in ["train", "val", "test"]:
    for cls in CLASSES:
        os.makedirs(os.path.join(TARGET_DIR, subset, cls), exist_ok=True)

for cls in CLASSES:
    class_dir = os.path.join(SOURCE_DIR, cls)
    images = [
        f for f in os.listdir(class_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    random.shuffle(images)

    total = len(images)
    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)

    train_imgs = images[:train_end]
    val_imgs = images[train_end:val_end]
    test_imgs = images[val_end:]

    print(f"\nClass: {cls}")
    print(f"Total: {total}")
    print(f"Train: {len(train_imgs)}, Val: {len(val_imgs)}, Test: {len(test_imgs)}")

    # move images
    for img in train_imgs:
        shutil.copy(
            os.path.join(class_dir, img),
            os.path.join(TARGET_DIR, "train", cls, img)
        )
    for img in val_imgs:
        shutil.copy(
            os.path.join(class_dir, img),
            os.path.join(TARGET_DIR, "val", cls, img)
        )
    for img in test_imgs:
        shutil.copy(
            os.path.join(class_dir, img),
            os.path.join(TARGET_DIR, "test", cls, img)
        )

print("\n✅ Dataset successfully split into train / val / test!")
