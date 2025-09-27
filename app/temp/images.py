from PIL import Image
import pilgram
import os
from pathlib import Path
import shutil

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "output"))
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))


def apply_filter(image_id: str, filter_name: str = "toaster"):
    image_path = UPLOAD_DIR / image_id / "original.jpg"
    image = Image.open(image_path)

    # get the filter function
    filter_func = getattr(pilgram, filter_name)
    filtered_image = filter_func(image)

    # save output
    directory_path = OUTPUT_DIR / image_id
    directory_path.mkdir(parents=True, exist_ok=True)

    file_path = directory_path / f"{filter_name}.jpg"
    filtered_image.save(file_path, format="JPEG")

    return filtered_image


def lossy_resize(image_path, width, height) -> Image.Image:
    img = Image.open(image_path)
    return img.resize((width, height), Image.Resampling.LANCZOS)


def scale_image(image_path: str, percent: float) -> Image.Image:
    img = Image.open(image_path)
    orig_w, orig_h = img.size

    factor = percent / 100.0
    new_w = int(orig_w * factor)
    new_h = int(orig_h * factor)

    return img.resize((new_w, new_h), Image.Resampling.LANCZOS)
