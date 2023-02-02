#!/usr/bin/env python3

import argparse
import os
import shutil
from multiprocessing import Pool

import albumentations as A
import cv2
import tqdm

from generate_data import NUM_WORKER, OUTPUT_DIR as INPUT_DIR

AUGMENT_OUTPUT_DIR = "data_augmented"
TRANSFORMATIONS = [
    A.Affine(translate_px={"y":10, "x":10}, scale=[0.5, 1.0], rotate=[-3,3], mode=1, always_apply=True),
    A.Perspective(always_apply=True),
    A.RandomBrightnessContrast(),
    A.RandomShadow(shadow_roi=(0, 0, 1, 1), num_shadows_upper=4, shadow_dimension=8),
    A.RandomSunFlare(flare_roi=(0, 0, 1, 1), src_radius=100),
    A.PixelDropout(),
    A.RGBShift(),
    A.MedianBlur(blur_limit=3,),
    A.ZoomBlur(max_factor=1.03)
]

def apply_transforms(img, transforms):
    """apply given transformations"""
    transform = A.Compose(transforms)

    transformed = transform(image=img)
    transformed_image = transformed["image"]

    return transformed_image

def augment_sample(i):
    """Generate a augmentations for a given sample and save it to disk"""
    orig_img_path = f"{INPUT_DIR}/{i}/staff_1.png"
    orig_txt_path = f"{INPUT_DIR}/{i}/staff_1.txt"
    orig_ly_path = f"{INPUT_DIR}/{i}/staff_1.ly"
    img = cv2.imread(orig_img_path)

    augmented_path = f"{AUGMENT_OUTPUT_DIR}/{i}"
    os.makedirs(augmented_path, exist_ok=True)

    new_img = apply_transforms(img, TRANSFORMATIONS)

    cv2.imwrite(os.path.join(augmented_path, f"staff_1.png"), new_img)
    shutil.copy(orig_txt_path, os.path.join(augmented_path, f"staff_1.txt"))
    shutil.copy(orig_ly_path, os.path.join(augmented_path, f"staff_1.ly"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Augmented data generation of input data.")
    parser.add_argument("--num_worker", type=int, required=False, help="Amount of workers that are used to generate the data.", default=NUM_WORKER)
    parser.add_argument("--input_dir", type=str, required=False, help="Folder for the input data.", default=INPUT_DIR)
    parser.add_argument("--augment_output_dir", type=str, required=False, help="Folder for the generated data.", default=AUGMENT_OUTPUT_DIR)

    args = parser.parse_args()
    NUM_WORKER = args.num_worker
    INPUT_DIR = args.input_dir
    AUGMENT_OUTPUT_DIR = args.augment_output_dir

    # Call augment_sample on ids with tqdm and multiprocessing
    with Pool(NUM_WORKER) as pool:
        list(tqdm.tqdm(pool.imap(augment_sample, os.listdir(INPUT_DIR)), total=len(os.listdir(INPUT_DIR))))
