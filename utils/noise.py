"""Noise functions for the captchas."""
from typing import Literal, Sequence

import sys
import random
import secrets

import numpy as np

from PIL import Image, ImageDraw, ImageFont


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


def TextAngled(
    img: Image.Image,
    xy: tuple[float, float],
    text: str | bytes,
    fill=None,
    font=None,
    anchor: str = None,
    spacing: float = 4,
    align: Literal["left", "center", "right"] = "left",
    direction: Literal["rtl", "ltr", "ttb"] = None,
    features: Sequence[str] = None,
    language: str = None,
    stroke_width: int = 0,
    stroke_fill=None,
    embedded_color: bool = False,
    angle: int = 0,
    position_from_center: bool = False,
):
    """Wrapper around ImageDraw but you can specify an angle for the text

    Args:
        img (PIL.Image.Image): The 'Image' to draw the text on
        xy (tuple[float, float]: x and y-axis coordinates for the text
        fill (Optional[Union[str, tuple[int]]): colour for the text
        angle (int, optional): The angle for how much to rotate the text. Defaults to 0.
        position_from_center (bool): If True, instead of rendering the text from top-left,
        the center of the text will be at 'xy'

    Returns:
        PIL.Image.Image: new 'Image' with the text on it
    """
    if not font:
        if sys.platform == "win32":
            font = ImageFont.truetype("arial.ttf", 48)
        else:
            font = ImageFont.load_default()

    # Create an ImageDraw object from the image
    draw = ImageDraw.Draw(img)

    # Get the size of the text
    text_width, text_height = draw.textsize(text, font=font)

    # Create a new image to hold the rotated text
    rotated_text_img = Image.new(
        mode="RGBA", size=(text_width, text_height), color=(0, 0, 0, 0)
    )

    rotated_text_draw = ImageDraw.Draw(rotated_text_img)

    rotated_text_draw.text(
        (0, 0),
        text,
        fill=fill,
        font=font,
        anchor=anchor,
        spacing=spacing,
        align=align,
        direction=direction,
        features=features,
        language=language,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
        embedded_color=embedded_color,
    )

    # Rotate the text image by 'angle'
    rotated_text_img = rotated_text_img.rotate(angle, expand=True)

    #! If 'position_from_center' == True, the text's center will be rendered at
    #! 'xy' instead of top-left
    pos = (
        (xy[0] - (rotated_text_img.width // 2), xy[1] - (rotated_text_img.height // 2))
        if position_from_center
        else xy
    )

    #! This code draws the text from its top left corner
    img.paste(rotated_text_img, pos, rotated_text_img)

    # return new 'Image', sadly I couldn't find a way to make it in-place :(
    return img
