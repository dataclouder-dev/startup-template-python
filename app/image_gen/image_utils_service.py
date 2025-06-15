from io import BytesIO

import requests
from PIL import Image


def transform_to_webp_bytes(image_io: BytesIO) -> BytesIO:
    pil_image = Image.open(image_io)
    img_webp_io = BytesIO()
    pil_image.save(img_webp_io, "webp")
    return img_webp_io


def download_image_to_memory(url: str) -> BytesIO:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful

    return BytesIO(response.content)
