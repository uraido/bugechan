"""
Functions to handle image processing such as downscaling, cropping, etc.
"""
from PIL import Image
import requests


def download_image(url: str):
    response = requests.get(url)
    if '.png' in url:
        extension = 'png'
    elif '.jpg' in url or '.jpeg' in url:
        extension = 'jpg'
    else:
        return None

    with open(f"image.{extension}", "wb") as f:
        f.write(response.content)
    return f"image.{extension}"


def scaling_algorithm(image: Image, min_size: int, max_size: int = None):
    if max_size is None:
        max_size = min_size

    # calculating img size
    width, height = image.size
    total_size = width * height

    # decrease bg img size if it is too big
    while total_size > max_size:
        image = image.resize((int(width * 0.9), int(height * 0.9)))

        width, height = image.size
        total_size = width * height

    # increase bg img size if it is too small
    while total_size < min_size:
        image = image.resize((int(width * 1.1), int(height * 1.1)))

        width, height = image.size
        total_size = width * height

    return image


def cropping_algorithm(image: Image, target_res: tuple):
    width, height = image.size
    target_width, target_height = target_res

    # returns if res equals target res
    if width == target_width and target_height == target_height:
        return image
    # cropping formula
    else:
        left = (width - target_width) // 2
        top = (height - target_height) // 2
        right = (width + target_width) // 2
        bottom = (height + target_height) // 2

        return image.crop(box=(left, top, right, bottom))