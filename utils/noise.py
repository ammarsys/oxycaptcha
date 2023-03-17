"""Noise functions for the captchas."""

import numpy as np
import secrets
import random

from PIL import Image, ImageDraw


def add_noise_lines(image: Image.Image) -> Image.Image:
    """Add noise lines to an image."""
    size = image.im.size

    for _ in range(secrets.randbelow(3)):
        x = (-50, -50)
        y = (size[0] + 10, secrets.choice(range(0, size[1] + 10)))

        image.arc(x + y, 0, 360, fill="white")

    return image


def salt_and_pepper(image: Image.Image, probability: float) -> Image.Image:
    """
    Adds white pixels to a PIL image with a specified probability.

    Args:
        image (PIL.Image): The input image.
        probability (float): The probability of adding a white pixel at each pixel location.

    Returns:
        PIL.Image: The output image with white pixels added.

    """
    output_image = Image.new(image.mode, image.size)

    draw = ImageDraw.Draw(output_image)

    for x in range(image.width):
        for y in range(image.height):
            random_number = secrets.choice((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1))

            if random_number < probability:
                draw.point((x, y), fill=(255, 255, 255))

            else:
                pixel = image.getpixel((x, y))
                draw.point((x, y), fill=pixel)

    return output_image


