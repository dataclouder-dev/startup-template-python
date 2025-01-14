from io import BytesIO
import requests
from PIL import Image


def transform_to_webp_bytes(image_io: BytesIO) -> BytesIO:
    # image_bytes = BytesIO(bytes)
    pil_image = Image.open(image_io)
    img_webp_io = BytesIO()
    pil_image.save(img_webp_io, "webp")
    # pil_image.save("test.webp", "webp")
    return img_webp_io

def download_image_to_memory(url) -> BytesIO:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful

    image_data = BytesIO(response.content)
    return image_data