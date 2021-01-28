from PIL import ImageTk, Image, ImageDraw
import numpy as np

def masking(img):
    img = img.convert('RGB')
    npImage = np.array(img)
    h, w = img.size

    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)

    npalpha = np.array(alpha)
    npImage = np.dstack((npImage, npalpha))
    ig = Image.fromarray(npImage)

    return ig
