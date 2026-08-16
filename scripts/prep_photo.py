import sys
import cv2
import numpy as np
from rembg import remove
from PIL import Image
import os

def prep_photo(input_path):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        sys.exit(1)

    print(f"Processing {input_path}...")
    
    # 1. Remove background
    with open(input_path, 'rb') as i:
        input_data = i.read()
        subject_data = remove(input_data)
    
    # rembg returns bytes of a PNG image. Save to a temporary file and read back
    temp_path = "temp_rembg.png"
    with open(temp_path, "wb") as o:
        o.write(subject_data)
    
    # Read back with cv2
    img_cv = cv2.imread(temp_path, cv2.IMREAD_UNCHANGED)
    os.remove(temp_path)

    # 2. Composite onto pure white
    # img_cv is BGRA
    alpha_channel = img_cv[:, :, 3]
    rgb_channels = img_cv[:, :, :3]

    # Create white background
    white_background = np.ones_like(rgb_channels, dtype=np.uint8) * 255

    # Alpha blending
    alpha_factor = alpha_channel[:, :, np.newaxis] / 255.0
    alpha_factor = np.concatenate([alpha_factor, alpha_factor, alpha_factor], axis=2)

    composited = rgb_channels * alpha_factor + white_background * (1 - alpha_factor)
    composited = composited.astype(np.uint8)

    # Convert to grayscale
    gray = cv2.cvtColor(composited, cv2.COLOR_BGR2GRAY)

    # 3. Boost local contrast with CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)

    # Save output
    output_path = "source-prepped.png"
    cv2.imwrite(output_path, enhanced)
    print(f"Saved prepped photo to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <source-photo.jpg>")
        sys.exit(1)
    prep_photo(sys.argv[1])
