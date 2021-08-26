from PIL import Image, ImageOps

def resize_images(path, new_width=256, new_height=256):
    pil_image = Image.open(path)
    if pil_image.width > new_width or pil_image.height > new_height:
        pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)
        pil_image_rgb = pil_image.convert("RGB")
        pil_image_rgb.save(path, format="JPEG", quality=90)
    return path