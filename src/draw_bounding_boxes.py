import os

from PIL import Image, ImageDraw, ImageFont

FONT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "../fonts/NotoSansJP-Bold.ttf"
)

def draw_bounding_boxes(image_path, faces):
    image = Image.open(image_path)
    image_width, image_height = image.size
    draw = ImageDraw.Draw(image)
    if not os.path.exists(FONT_PATH):
        raise FileNotFoundError(f"Font file not found: {FONT_PATH}")

    font_size = max(image_width, image_height) // 50
    text_ascend = font_size / 2.5
    font = ImageFont.truetype(FONT_PATH, font_size)

    for idx, face in enumerate(faces):
        bbox = face["BoundingBox"]
        _draw(
            idx,
            draw,
            image_width,
            image_height,
            bbox,
            font,
            text_ascend
        )

    return image


def _draw(
        idx: int,
        draw: ImageDraw,
        image_width,
        image_height,
        bbox,
        font,
        text_ascend
    ):

    left = bbox['Left'] * image_width
    top = bbox['Top'] * image_height
    right = left + (bbox['Width'] * image_width)
    bottom = top + (bbox['Height'] * image_height)
    
    draw.rectangle([left, top, right, bottom], outline="red", width=3)

    _draw_caption(idx, draw, font, left, top, text_ascend)


def _draw_caption(idx, draw, font, left, top, text_ascend):
    label = f"選手{idx + 1}"
    text_bbox = draw.textbbox((0, 0), label, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_background = [(left, top - text_height - 5), (left + text_width + 4, top)]
    draw.rectangle(text_background, fill="red")

    draw.text((left + 2, top - text_height - text_ascend), label, fill="black", font=font)
    