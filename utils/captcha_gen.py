import random
import secrets
import os

from PIL import ImageDraw, Image, ImageFont

from utils import noise


FONTS_LOWER = [
    ImageFont.truetype(os.path.join("fonts", "lower", "gadugib.ttf"), 34),
    ImageFont.truetype(os.path.join("fonts", "lower", "Chalkduster_400.ttf"), 34),
    ImageFont.truetype(
        os.path.join("fonts", "lower", "ShadowsIntoLight-Regular.ttf"), 34
    ),
    ImageFont.truetype(os.path.join("fonts", "lower", "Rajdhani-SemiBold.ttf"), 34),
]

FONTS_UPPER = [
    ImageFont.truetype(os.path.join("fonts", "upper", "arial.ttf"), 57),
    ImageFont.truetype(os.path.join("fonts", "upper", "FallingSky-JKwK.ttf"), 57),
    ImageFont.truetype(os.path.join("fonts", "upper", "TrainOne-Regular.ttf"), 57),
    ImageFont.truetype(os.path.join("fonts", "upper", "BebasNeue-Regular.ttf"), 57),
]


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
    space, height = random.randint(20, 25), random.randint(9, 17)

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

        angle = secrets.choice(range(-20, 20))
        img = noise.text_angled(
            img, cords, letter, fill=white, font=corresponding_font[letter], angle=angle
        )

        space += relative_spacing + secrets.choice(range(7, 13))
        height += secrets.choice((-1, 1))

        text_positions.append(tuple(secrets.randbelow(10) + 15 + i for i in cords))

    d = noise.add_noise_lines(ImageDraw.Draw(img))

    # Add a noise line relative to the text position
    value = secrets.randbelow(len(text_positions))
    for i in range(len(text_positions) - value):
        d.line((text_positions[i], text_positions[i + value]), fill=white, width=0)  # type: ignore

    return noise.salt_and_pepper(img, probability=0.2)
