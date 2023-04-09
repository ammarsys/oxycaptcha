"""Captcha generation for the API (this is where the magic happens!)"""

import random
import secrets
import os
import math

from PIL import ImageDraw, Image, ImageFont


FONTS_LOWER = [
    ImageFont.truetype(os.path.join("fonts", "lower", "gadugi-bold.ttf"), 30),
    ImageFont.truetype(os.path.join("fonts", "lower", "Chalkduster_400.ttf"), 34),
    ImageFont.truetype(os.path.join("fonts", "lower", "RobotoSlab-Black.ttf"), 34),
]

FONTS_UPPER = [
    ImageFont.truetype(os.path.join("fonts", "upper", "arial.ttf"), 60),
    ImageFont.truetype(os.path.join("fonts", "upper", "FallingSky-JKwK.ttf"), 60),
    ImageFont.truetype(os.path.join("fonts", "upper", "TrainOne-Regular.ttf"), 60),
    ImageFont.truetype(os.path.join("fonts", "upper", "BebasNeue-Regular.ttf"), 60),
]


def add_noise_lines(image: ImageDraw.ImageDraw) -> ImageDraw.ImageDraw:
    """Add noise lines to an image."""
    size = image.im.size  # type: ignore

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
            random_number = secrets.choice(
                (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1)
            )

            if random_number < probability:
                draw.point((x, y), fill=(255, 255, 255))

            else:
                pixel = image.getpixel((x, y))
                draw.point((x, y), fill=pixel)

    return output_image


def find_coeffs(angle):
    if secrets.choice((0, 1)):
        angle = math.radians(angle)
    else:
        angle = -math.radians(angle)

    coeffs = [1, 0, 0, math.tan(angle), 1, 0, 0, 0, 1]

    return coeffs


def text_angled(
    img,
    xy: tuple[int, int],
    text: str,
    fill: tuple[int, int, int] | str,
    font: ImageFont.FreeTypeFont,
    rot_angle: int,
    tilt_angle: int,
    **kwargs
):
    """Wrapper around ImageDraw but you can specify an angle for the text

    Args:
        img (PIL.Image.Image): The 'Image' to draw the text on
        rot_angle (int, optional): The angle for how much to rotate the text. Defaults to 0.
        font (ImageFont.FreeTypeFont): font for the text
        fill (tuple[int, int, int] | str): colour for the text
        text (str): the text itself
        xy (tuple[int, int]: coordinates for the text
        tilt_angle (int): horizontal tilt for the text

    Returns:
        PIL.Image.Image: new 'Image' with the text on it

    """
    draw = ImageDraw.Draw(img)

    text_width, text_height = draw.multiline_textsize(text, font=font)

    # Create new image for the font
    rotated_text_img = Image.new(
        mode="RGBA", size=(text_width + 100, text_height + 100), color=(0, 0, 0, 0)
    )
    rotated_text_draw = ImageDraw.Draw(rotated_text_img)
    rotated_text_draw.text((0, 0), text, fill=fill, font=font, **kwargs)

    coeffs = find_coeffs(tilt_angle)
    rotated_text_img = rotated_text_img.transform(
        (
            int(rotated_text_img.width + abs(coeffs[1] * rotated_text_img.height)),
            rotated_text_img.height,
        ),
        Image.AFFINE,
        coeffs,
        Image.BICUBIC,
    )
    rotated_text_img = rotated_text_img.rotate(rot_angle, expand=True)

    img.paste(rotated_text_img, xy, rotated_text_img)

    return img


def cap_gen(text: str) -> Image.Image:
    """
    Generates an image of a captcha using the given 'text'.

    Args:
        text (str): The captcha text to be used for generating the captcha image.

    Returns:
        Image.Image: An image of the captcha generated using the given 'text'.

    """
    # Start with a random height and spacing
    white = 255, 255, 255
    space, height = random.randint(20, 25), random.randint(5, 13)

    # Assign every letter a corresponding random font
    corresponding_font = {
        let: secrets.choice(FONTS_UPPER if let.isupper() else FONTS_LOWER)
        for let in text
    }
    text_positions = []

    img = Image.new("RGB", (300, 100), color=(128, 128, 128))
    img.load()

    # Use relative spacing so that there isn't much of empty space on either of sides
    relative_spacing = 200 // len(text)

    for count, letter in enumerate(text):
        cords = space, height

        rot_angle = secrets.choice(range(-10, 10))
        tilt_angle = secrets.choice(range(10, 30))
        img = text_angled(
            img,
            cords,
            letter,
            fill=white,
            font=corresponding_font[letter],
            rot_angle=rot_angle,
            tilt_angle=tilt_angle,
        )

        space += relative_spacing + secrets.choice(range(7, 13))
        height += secrets.choice((-1, 1))

        text_positions.append(tuple(secrets.randbelow(10) + 15 + i for i in cords))

    d = add_noise_lines(ImageDraw.Draw(img))

    # Add a noise line relative to the text position
    value = secrets.randbelow(len(text_positions))
    for i in range(len(text_positions) - value):
        d.line((text_positions[i], text_positions[i + value]), fill=white, width=0)  # type: ignore

    return salt_and_pepper(img, probability=0.2)
