import os
import shutil
import random

SOURCE = "DatasetBinary"
DEST = "DatasetBinary_split"
CLASSES = ["Healthy", "Damaged"]

random.seed(42)

for split in ["train", "val", "test"]:
    for cls in CLASSES:
        os.makedirs(os.path.join(DEST, split, cls), exist_ok=True)

# Split each class
for cls in CLASSES:
    src_folder = os.path.join(SOURCE, cls)
    imgs = [f for f in os.listdir(src_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    random.shuffle(imgs)
    n = len(imgs)

    train_end = int(n * 0.7)
    val_end = int(n * 0.85)

    train_files = imgs[:train_end]
    val_files = imgs[train_end:val_end]
    test_files = imgs[val_end:]

    for split_name, file_list in zip(["train", "val", "test"], [train_files, val_files, test_files]):
        for file in file_list:
            shutil.copy(os.path.join(src_folder, file), os.path.join(DEST, split_name, cls, file))

print("🎉 Done! DatasetBinary_split is ready.")
