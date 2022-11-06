"""
Utility for generating Notion header images that
function as thumbnails when combined with the gallery
view of a Notion database

For optimization across different device screens,
the ideal image dimensions are 1500px x 600px with
primary content centered within 1170px x 230px
"""
import json
import random
from PIL import Image, ImageDraw, ImageFont

colors = {
    "blank": {
        "c": (0, 0, 0),
        "p_font": "rgb(255, 255, 255)",
        "s_font": "rgb(255, 255, 255)",
    },
    "light_blue": {
        "c": (0, 0, 0),
        "p_font": "rgb(135, 206, 250)",
        "s_font": "rgb(135, 206, 250)",
    },
    "dark_green": {
        "c": (0, 0, 0),
        "p_font": "rgb(3, 125, 70)",
        "s_font": "rgb(3, 125, 70)",
    },
    "orange": {
        "c": (0, 0, 0),
        "p_font": "rgb(255, 165, 0)",
        "s_font": "rgb(255, 165, 0)",
    },
}


def rand_color():
    """
    return a random key from dictionary
    of colors for text
    """
    return random.choice(list(colors.keys()))


def add_color(image, color, transparency):
    '''
    Take in an image and apply color and
    opacity changes, return new image
    '''
    applied_color = Image.new("RGB", image.size, color)
    applied_mask = Image.new("RGBA", image.size, (0, 0, 0, transparency))
    return Image.composite(image, applied_color, applied_mask).convert("RGB")


def center_text(img, font, text1, text2, fill1, fill2):
    draw = ImageDraw.Draw(img)
    width, height = img.size
    t1_width = draw.textlength(text1, font)
    t2_width = draw.textlength(text2, font)
    point_one = ((width - t1_width) / 2, height // 3)
    point_two = ((width - t2_width) / 2, height // 3 + height // 5)
    draw.text(point_one, text1, fill=fill1, font=font)
    draw.text(point_two, text2, fill=fill2, font=font)
    return img


def add_text(
    img,
    color,
    text1,
    text2,
    logo=False,
    font="static/RobotoMono-Bold.ttf",
    font_size=50,
):
    draw = ImageDraw.Draw(img)

    p_font = color["p_font"]
    s_font = color["s_font"]

    # starting position of the message
    img_w, img_h = img.size
    height = img_h // 3
    font = ImageFont.truetype(font, size=font_size)

    if logo == False:
        center_text(img, font, text1, text2, p_font, s_font)
    else:
        text1_offset = (img_w // 4, height)
        text2_offset = (img_w // 4, height + img_h // 5)
        draw.text(text1_offset, text1, fill=p_font, font=font)
        draw.text(text2_offset, text2, fill=s_font, font=font)
    return img


def add_logo(background, foreground):
    bg_h = background.size[1]
    img_h = foreground.size[1]
    img_offset = (20, (bg_h - img_h) // 2)
    background.paste(foreground, img_offset, foreground)
    return background


def write_image(background, color, text1, text2, foreground=""):
    background = add_color(background, color["c"], 255)
    if not foreground:
        add_text(background, color, text1, text2)
    else:
        add_text(background, color, text1, text2, logo=True)
        add_logo(background, foreground)
    return background


if __name__ == "__main__":
    try:
        with open("config.json", "r") as file:
            config = json.loads(file.read())
    except IOError:
        print("There was an error opening the file `config.json`")

    print(f"config loaded:\n{json.dumps(config, indent=2)}")

    img_name = config.get("imageName")
    text1 = config.get("text")[0]
    text2 = config.get("text")[1]
    color = config.get("color")
    font = config.get("font")
    background_file = config.get("background")
    background = Image.open(background_file)
    # foreground = Image.open("Lorenz.png")

    if color == "random":
        color = rand_color()
        print(f"new color is {color}")

    background = write_image(background, colors[color], text1, text2, foreground="")
    background.save(img_name)
