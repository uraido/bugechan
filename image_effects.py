from PIL import Image
from image_handling import scaling_algorithm, cropping_algorithm


def mugify_image(background: str, overlay: str):

    # opening background image
    background_img = Image.open(background)

    # Opening the secondary image (overlay image)
    overlay_img = Image.open(overlay)

    # upscale/downscale image depending on size
    background_img = scaling_algorithm(background_img, 720 * 720, 1280 * 720)

    # cropping bg img
    background_img = cropping_algorithm(background_img, (720, 720))

    # Pasting overlay_img on top of template_img
    background_img.paste(overlay_img, (0, 0), mask=overlay_img)

    # Displaying the image
    background_img.save(fp='overlayed.png')


def approve_image(main_image: str):
    background = Image.new('RGB', (556, 689))
    image = Image.open(main_image)

    # opening layer res = 556x689 bounding box res = 186x256 box top left = 100, 317
    layer = Image.open('images/approve/layer.png')

    # upscale/downscale image
    image = scaling_algorithm(image, 186 * 256)

    # crop image
    image = cropping_algorithm(image, (186, 256))

    # paste image on template
    background.paste(image, (100, 317))

    # paste layer over image on template
    background.paste(layer, (0, 0), mask=layer)
    background.save(fp='overlayed.png')


if __name__ == '__main__':
    approve_image('images/test_image.jpg')
