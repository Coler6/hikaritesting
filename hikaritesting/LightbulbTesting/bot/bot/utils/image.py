from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageColor
import PIL.Image
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import binascii

def add_text(im, text, position):
        fnt = ImageFont.truetype("/home/container/font/ERAS.ttf", 25)
        txt = PIL.Image.new("RGBA", im.size, color=(255, 255, 255, 0))
        d = ImageDraw.Draw(txt)
        d.text(position, text, font=fnt, fill=(0, 0, 0, 255))
        im.alpha_composite(txt)
        return im
        
def get_icon(pfp):
    icon = pfp
    size = (200,200)
    icon = icon.resize((200, 200))
    mask = PIL.Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0) + size, fill=255)
    out = ImageOps.fit(pfp.convert("RGBA"), mask.size, centering=(.5,.5))
    out.putalpha(mask)
    return out
        
def get_text(text, position, size):
        fnt = ImageFont.truetype("/home/container/font/ERAS.ttf", size)
        txt = PIL.Image.new("RGBA", (500, 100), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(txt)
        draw.text((0, 0), text, font=fnt, fill=(255, 255, 255, 255))
        return txt
def get_smol_text(text, position):
        fnt = ImageFont.truetype("/home/container/font/arial.ttf", 25)
        txt = PIL.Image.new("RGBA", (500, 100), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(txt)
        draw.text((0, 0), text, font=fnt, fill=(255, 255, 255, 255))
        return txt
    
def get_color(pfp):
    NUM_CLUSTERS = 5
    pfp = pfp.resize((75, 75))
    ar = np.asarray(pfp)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    vecs, dist = scipy.cluster.vq.vq(ar, codes)
    counts, bins = scipy.histogram(vecs, len(codes))
    index_max = scipy.argmax(counts)
    peak = codes[index_max]
    color = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    return color

def create_welcome_card(pfp, user):
    base = PIL.Image.new("RGBA", (900, 250), color=(28, 28, 28, 255))
    icon = get_icon(pfp)
    text = user.name
    if len(text) <= 10:
            size = 80
            pos_y = 25
    elif len(text) <= 15:
            pos_y = 45
            size = 70
    elif len(text) <= 25:
            pos_y = 60
            size = 40
    elif len(text) <= 32:
        pos_y = 75
        size = 50
    fnt = ImageFont.truetype("/home/container/font/ERAS.ttf", size)
    fnt2 = ImageFont.truetype("/home/container/font/arial.ttf", 25)
    color = get_color(pfp)
    color = ImageColor.getcolor(f"#{color}", "RGB")
    print(color)
    colour = str(color)
    colour = colour.replace("(", "")
    colour = colour.replace(")", "")
    colour_red = colour.split(",")[0]
    print("1")
    if color <= (0, 0, 30):
        color = (0, 0, 30)
    elif color <= (30, 30, 30):
        pass
    elif color <= (30, 30, 30):
        pass
    side = ImageDraw.Draw(base)
    side.rectangle([(0,0),(225, 250)], fill = color)
    side.polygon([(150, 250), (260, 250), (225,0)], fill = color)
    base.alpha_composite(icon, (25, 25))
    W = 900
    name = user.name
    name = name.replace(" ", "")
    print(name)
    w, h = side.textsize(name, font=fnt)
    print(w,h)
    x = ((W-w)/2)+100
    x = round(x)
    print(x)
    print(text)
    text = get_text(text, (50, pos_y), size)
    print(text)
    base.alpha_composite(text, (x, 10))
    W = 900
    w, h = side.textsize(f"Welcome to {user.guild.name}!", font=fnt2)
    x = ((W-w)/2)+100
    x = round(x)
    text = get_smol_text(f"Welcome to {user.guild.name}!", (50, 25))
    base.alpha_composite(text, (x, 90))
    return base