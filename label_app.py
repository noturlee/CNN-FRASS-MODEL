import os
import shutil
import random
import streamlit as st
from PIL import Image



CROPS_DIR = "DatasetB/crops_v2"
OUTPUT_DIR = "DatasetB"

CLASS_NAMES = ["Healthy", "Diseased", "Pests"]

# Create class folders if they don't exist
for cls in CLASS_NAMES:
    os.makedirs(os.path.join(OUTPUT_DIR, cls), exist_ok=True)

# Load all remaining unlabeled images
def get_unlabeled_images():
    return sorted([
        f for f in os.listdir(CROPS_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])



st.set_page_config(page_title="Lettuce Labeling Tool", layout="centered")
st.title("🥬 Lettuce Crop Labeling Tool")
st.write("Label each crop using your expert judgment.")

unlabeled = get_unlabeled_images()

if len(unlabeled) == 0:
    st.success("🎉 All images are labeled!")
    st.stop()

# Choose image: RANDOM or SEQUENTIAL
MODE = "RANDOM"   # change to "SEQUENTIAL" if you prefer order

if MODE == "RANDOM":
    image_file = random.choice(unlabeled)
else:
    image_file = unlabeled[0]   # smallest filename first

image_path = os.path.join(CROPS_DIR, image_file)

# Display crop
img = Image.open(image_path)
st.image(img, caption=image_file, use_container_width=True)

st.write("### What is this plant's status?")
col1, col2, col3 = st.columns(3)



def move_image(label):
    src = image_path
    dst = os.path.join(OUTPUT_DIR, label, image_file)
    shutil.move(src, dst)
    st.rerun()


with col1:
    if st.button("🌱 Healthy"):
        move_image("Healthy")

with col2:
    if st.button("🟠 Diseased"):
        move_image("Diseased")

with col3:
    if st.button("🐛 Pests"):
        move_image("Pests")

#streamlit run label_app.py
