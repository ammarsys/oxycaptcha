"""Noise functions for the captchas."""

import numpy as np
import secrets

from PIL import Image


def add_noise_lines(image: Image.Image) -> Image.Image:
    """Add noise lines to an image."""
    size = (305, 95)

    for _ in range(1):
        width = secrets.choice((1, 2))
        start = (0, secrets.choice(range(0, size[1] - 1)))
        end = (size[0], secrets.choice(range(0, size[1] - 1)))
        image.line([start, end], fill="white", width=width)

    for _ in range(1):
        start = (-50, -50)
        end = (size[0] + 10, secrets.choice(range(0, size[1] + 10)))
        image.arc(start + end, 0, 360, fill="white")

    return image


def salt_and_pepper(image: Image.Image, prob: float) -> Image.Image:
    """Add the "salt and pepper" effect to an image."""
    arr = np.asarray(image)  # type: ignore
    original_dtype = arr.dtype
    intensity_levels = 2 ** (arr[0, 0].nbytes * 8)
    min_intensity = 0
    max_intensity = intensity_levels - 1
    random_image_arr = np.random.choice(
        [min_intensity, 1, np.nan], p=[prob / 2, 1 - prob, prob / 2], size=arr.shape
    )
    salt_and_peppered_arr = arr.astype(np.float_) * random_image_arr
    salt_and_peppered_arr = np.nan_to_num(
        salt_and_peppered_arr, nan=max_intensity
    ).astype(original_dtype)

    return Image.fromarray(salt_and_peppered_arr)
