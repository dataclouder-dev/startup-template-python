import fal_client

from app.image_gen import image_utils_service


def generate_image(prompt: str, settings: dict | None = None) -> str:
    if settings is None:
        settings = {}
    print("Generating image")

    image_size = {"width": settings.get("resolution").get("w"), "height": settings.get("resolution").get("h")} if settings.get("resolution") else {"width": 720, "height": 1280}

    model = settings.get("model", "fal-ai/playground-v25")
    print("resolution", image_size, "model", model)

    handler = fal_client.submit(
        model,
        arguments={
            "prompt": prompt,
            "image_size": image_size,
            "num_inference_steps": 30,
        },
    )

    result = handler.get()
    url = result["images"][0]["url"]
    print(result)
    return url


def generate_image_and_get_bytes(prompt: str, settings: dict | None = None) -> bytes:
    if settings is None:
        settings = {}
    url = generate_image(prompt, settings)
    img_io = image_utils_service.download_image_to_memory(url)
    img_webp_io = image_utils_service.transform_to_webp_bytes(img_io)
    return img_webp_io.getvalue()
