import random
import secrets
import os

from PIL import ImageDraw, Image, ImageFont

from utils import noise


FONTS_LOWER = [
    ImageFont.truetype(os.path.join("fonts", "lower", "gadugib.ttf"), 32),
    ImageFont.truetype(os.path.join("fonts", "lower", "Chalkduster_400.ttf"), 32),
    ImageFont.truetype(os.path.join("fonts", "lower", "ShadowsIntoLight-Regular.ttf"), 32),
    ImageFont.truetype(os.path.join("fonts", "lower", "Rajdhani-SemiBold.ttf"), 32),
]

FONTS_UPPER = [
    ImageFont.truetype(os.path.join("fonts", "upper", "arial.ttf"), 55),
    ImageFont.truetype(os.path.join("fonts", "upper", "FallingSky-JKwK.ttf"), 55),
    ImageFont.truetype(os.path.join("fonts", "upper", "TrainOne-Regular.ttf"), 55),
    ImageFont.truetype(os.path.join("fonts", "upper", "BebasNeue-Regular.ttf"), 55),
]


def cap_gen(text: str) -> Image.Image:
    """
    Generates an image of a captcha using the given 'text'.

    Args:
        text (str): The captcha text to be used for generating the captcha image.

    Returns:
        Image.Image: An image of the captcha generated using the given 'text'.
    """
    white = 255, 255, 255
    space, height = random.randint(5, 10), random.randint(5, 10)

    corresponding_font = {
        let: random.choice(FONTS_UPPER if let.isupper() else FONTS_LOWER)
        for let in text
    }
    text_positions = []

    img = Image.new("RGB", (300, 100), color=(128, 128, 128))
    img.load()

    d = noise.add_noise_lines(ImageDraw.Draw(img))

    for count, letter in enumerate(text):
        cords = space, height
        d.text(cords, f"{letter}", fill=white, font=corresponding_font[letter])

        space += secrets.choice(range(35, 45))
        height += secrets.choice(range(1, 11))

        text_positions.append(tuple(secrets.randbelow(10) + 15 + i for i in cords))

    value = secrets.randbelow(len(text_positions))
    for i in range(len(text_positions) - value):
        d.line((text_positions[i], text_positions[i + value]), fill=white, width=0)

    return img
