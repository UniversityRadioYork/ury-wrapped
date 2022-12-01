from PIL import Image, ImageFont, ImageDraw
import os.path
import textwrap


def generate_image(text: str, template="img/template.png"):
    im = Image.open(os.path.join(os.path.dirname(__file__), template))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(
        os.path.join(os.path.dirname(__file__), "img/Raleway-Bold.ttf"), 50
    )
    w, h = draw.textsize(text, font=font)
    margin = offset = 128
    for line in textwrap.wrap(text, width=30):
        draw.text((margin, offset), line, font=font, fill="#000000")
        offset += font.getsize(line)[1]
    return im


def make_image(text: str, output_path: str, template="img/template.png"):
    generate_image(text, template).convert("RGB").save(output_path)
