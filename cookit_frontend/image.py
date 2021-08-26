import math
from uuid import uuid1
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageColor, ImageFont
import streamlit as st
import numpy as np


@st.cache
def save_uploaded_file(filename, bytes_image):
    # create folder if not exists for uploaded images
    Path("./uploaded_files").mkdir(parents=True, exist_ok=True)
    file_location = f"./uploaded_files/{filename}_{uuid1()}"

    with open(file_location, "wb") as f:
        f.write(bytes_image.getbuffer())

    file_path = resize_image(file_location)
    return file_path


@st.cache
def resize_image(path, new_width=512, new_height=512):
    pil_image = Image.open(path)
    if pil_image.width > new_width or pil_image.height > new_height:
        #pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)
        #pil_image_rgb = pil_image.convert("RGB")
        pil_image.thumbnail((new_width, new_height), Image.ANTIALIAS)
        pil_image.save(path, format="JPEG", quality=90)
    return path


def draw_bounding_box_on_image(image_pil,
                               ymin,
                               xmin,
                               ymax,
                               xmax,
                               color,
                               font,
                               thickness=4,
                               display_str_list=()):
    """Adds a bounding box to an image."""
    draw = ImageDraw.Draw(image_pil)
    im_width, im_height = image_pil.size
    (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                  ymin * im_height, ymax * im_height)
    draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
                (left, top)],
                width=thickness,
                fill=color)

    # If the total height of the display strings added to the top of the bounding
    # box exceeds the top of the image, stack the strings below the bounding box
    # instead of above.
    display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
    # Each display_str has a top and bottom margin of 0.05x.
    total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

    if top > total_display_str_height:
        text_bottom = top
    else:
        text_bottom = top + total_display_str_height
    # Reverse list and print from bottom to top.
    for display_str in display_str_list[::-1]:
        text_width, text_height = font.getsize(display_str)
        margin = math.ceil(0.05 * text_height)
        draw.rectangle([(left, text_bottom - text_height - 2 * margin),
                        (left + text_width, text_bottom)],
                        fill=color)
        draw.text((left + margin, text_bottom - text_height - margin),
                display_str,
                fill="black",
                font=font)
        text_bottom -= text_height - 2 * margin


@st.cache
def draw_boxes(image_path, boxes, class_names, scores, max_boxes=10, min_score=0.1):
    """Overlay labeled boxes on an image with formatted scores and label names."""
    colors = list(ImageColor.colormap.values())
    font = ImageFont.load_default()
    boxes = np.array(boxes)
    image_pil = Image.open(image_path)

    for i in range(min(len(class_names), max_boxes)):
        if scores[i] >= min_score:
            ymin, xmin, ymax, xmax = tuple(boxes[i])
            display_str = "{}: {}%".format(class_names[i],
                                            int(100 * scores[i]))
            color = colors[hash(class_names[i]) % len(colors)]
            draw_bounding_box_on_image(
                image_pil,
                ymin,
                xmin,
                ymax,
                xmax,
                color,
                font,
                display_str_list=[display_str])
            #image_pil.save(image, format="JPEG", quality=90)
    return image_pil
