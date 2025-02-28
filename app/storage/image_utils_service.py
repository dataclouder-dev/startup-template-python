from io import BytesIO
from typing import Union

import numpy as np
import requests
from PIL import Image


def transform_to_webp_bytes(image_data: Union[BytesIO, bytes, np.ndarray]) -> BytesIO:
    # Handle numpy array (from cv2/matplotlib frames)
    if isinstance(image_data, np.ndarray):
        if isinstance(image_data, np.ndarray):
            # Convert BGR to RGB before creating PIL Image
            if len(image_data.shape) == 3 and image_data.shape[2] == 3:  # Check if it's a color image
                image_data = image_data[:, :, ::-1]  # BGR to RGB conversion
            pil_image = Image.fromarray(image_data)
    else:
        # Handle BytesIO or bytes as before
        if isinstance(image_data, bytes):
            image_data = BytesIO(image_data)
        pil_image = Image.open(image_data)

    img_webp_io = BytesIO()
    pil_image.save(img_webp_io, "webp")
    return img_webp_io


def download_image_to_memory(url: str) -> BytesIO:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful

    image_data = BytesIO(response.content)
    return image_data
