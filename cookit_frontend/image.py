import math
import io
import itertools
from uuid import uuid1
from pathlib import Path
from PIL import Image, ImageDraw, ImageColor, ImageFont
import streamlit as st
import numpy as np
from termcolor import colored
from io import BytesIO


@st.cache
def save_uploaded_file(filename, bytes_image):
    # create folder if not exists for uploaded images
    Path("./uploaded_files").mkdir(parents=True, exist_ok=True)
    file_location = f"./uploaded_files/{filename}_{uuid1()}"

    with open(file_location, "wb") as f:
        f.write(bytes_image.getbuffer())

    file_path = resize_image(file_location)
    return file_path


def resize_image(image_buffer, max_width=800, max_height=800):
    """ Resizes an PIL.Image type to a given max width or height
        Returns the resized PIL.Image object
    """
    pil_image = Image.open(image_buffer)
    if pil_image.width > max_width or pil_image.height > max_height:
        # Using the thumbnal mehtod makes sure we keep the original aspect ratio
        pil_image.thumbnail((max_width, max_height), Image.ANTIALIAS)
    return pil_image


def pil_to_buffer(pil_image):
    """ Takes image as returned by PIL.Image.open() and writes bytes to a buffer
        object since we cannot use the PIL image directly for our POST request but
        rather only a buffer or 'file-like' object.
    """
    buffer = io.BytesIO()
    pil_image.save(buffer, pil_image.format)
    buffer.seek(0)
    return buffer


def draw_bounding_box_on_image(image_pil, ymin, xmin, ymax, xmax, color,font,
                               thickness=4, display_str_list=()):
    """Adds a bounding box to an image."""
    draw = ImageDraw.Draw(image_pil)
    im_width, im_height = image_pil.size
    (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                  ymin * im_height, ymax * im_height)
    draw.line([(left, top), (left, bottom), (right, bottom), (right, top), (left, top)],
              width=thickness, fill=color)

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
                fill=decide_font_color(color),
                font=font)
        text_bottom -= text_height - 2 * margin


def _font_as_bytes():
    with open('font/Roboto-Medium.ttf', 'rb') as f:
        font_bytes = BytesIO(f.read())
    return font_bytes


def _calc_yiq(hex_color):
    r = int(hex_color[1:3], base=16)
    g = int(hex_color[3:5], base=16)
    b = int(hex_color[5:8], base=16)
    yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000
    return yiq


def decide_font_color(hex_color):
    """ Returns white/black depending on hex_color to make text on bboxes better
        readable for all appearing colors. Found in
        https://gomakethings.com/dynamically-changing-the-text-color-based-on-background-color-contrast-with-vanilla-js/#checking-color-contrast-with-vanillia-js
    """
    yiq = _calc_yiq(hex_color)
    if yiq >= 128:
        return 'black'
    return 'white'


#@st.cache
def draw_boxes(image_pil, boxes, class_names, scores):
    """Overlay labeled boxes on an image with formatted scores and label names."""
    colors = list(ImageColor.colormap.values())

    try:
        #font = ImageFont.truetype('Arial', 18)
        font = ImageFont.truetype(_font_as_bytes(), 20)
    except:
        print("Did not find requested font. Use default one")
        font = ImageFont.load_default()

    boxes = np.array(boxes)

    # combine data to dict where each score and bbox ccordinates are in a tuple
    data = {}
    for i, name in enumerate(class_names):
        data[name] = (boxes[i], scores[i])
    if len(boxes) > 1:
        filtered_data = find_overlapping_bboxes(data)
    else:
        filtered_data = data
    print(colored(f"Draw boxes for {filtered_data}", 'magenta'))

    # Now draw bbox for every class
    for ingr, data in filtered_data.items():
        ymin, xmin, ymax, xmax = tuple(data[0])
        display_str = "{}: {}%".format(ingr, int(100 * data[1]))
        color = colors[hash(ingr) % len(colors)]
        draw_bounding_box_on_image(image_pil, ymin, xmin, ymax, xmax, color,
                                    font, display_str_list=[display_str])
    return image_pil


def find_overlapping_bboxes(data, threshold=0.9):
    """ A probably not yet perfect solution to avoid overlapping bounding boxes by calculating
        the IoU value of each combination. Due to the order of combinations, the whole deletion
        and adding iteration is probably not perfectly working for all cases.
    """
    filtered_data = {}
    drop_list = []
    # returns list of tuples with all possible combinations between keys in data dict
    class_combinations = list(itertools.combinations(data, 2))
    for combo in class_combinations:
        iou = get_iou(data[combo[0]][0], data[combo[1]][0])
        if iou > threshold: # if too much overlap, add only the one with higher score
            print(colored(f"Found overlap between {combo[0]}: {data[combo[0]]} and {combo[1]}: {data[combo[1]]}", 'yellow'))
            if data[combo[0]][1] >= data[combo[1]][1]:
                filtered_data[combo[0]] = data[combo[0]]
                drop_list.append(combo[1])
            else:
                filtered_data[combo[1]] = data[combo[1]]
                drop_list.append(combo[0])
        else: # if overlap is small, add both
            filtered_data[combo[0]] = data[combo[0]]
            filtered_data[combo[1]] = data[combo[1]]
        #print(f"Keys in dict after iteration: {filtered_data.keys()}")

    # Now remove all overlapping bboxes with pairwise lower score from dict
    for key in drop_list:
        print(f"Remove {key} from filtered dict..")
        try:
            del filtered_data[key]
        except:
            pass
    return filtered_data

def get_iou(bb1, bb2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters
    ----------
    bb1 : list [ymin, xmin, ymax, xmax]
    bb2 : list [ymin, xmin, ymax, xmax]

    Returns
    -------
    float
        in [0, 1]
    """
    assert bb1[0] < bb1[2]
    assert bb1[1] < bb1[3]
    assert bb2[0] < bb2[2]
    assert bb2[1] < bb2[3]

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1[0], bb2[0])
    y_top = max(bb1[1], bb2[1])
    x_right = min(bb1[2], bb2[2])
    y_bottom = min(bb1[3], bb2[3])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1[2] - bb1[0]) * (bb1[3] - bb1[1])
    bb2_area = (bb2[2] - bb2[0]) * (bb2[3] - bb2[1])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou
