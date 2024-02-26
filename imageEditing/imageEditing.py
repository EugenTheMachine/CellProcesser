import numpy as np
import cv2
from PIL import Image as im, ImageFilter, ImageChops
from imageEditing.filter import *

# pd.df
# plt.plot

# TODO
def applyFilter(image, filter: Filter):
    # image = im.open(img_path)
    kernel = ImageFilter.Kernel((filter.shape, filter.shape), filter.kernel, scale=filter.scale)
    result = ImageChops.add(image.filter(kernel), im.new('RGB', image.size, (filter.move, filter.move, filter.move)))
    return result

def gammaCorrect(img, f):  # img = width x height x 3 array, f = 10-pow interpolation curve
    img = img / 255.0
    result = f(img)
    return result * 255.0
