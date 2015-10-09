import numpy as np
from PIL import Image


def toArray(image):
    return np.array(image)


def transform(image):
    return image

def zoom(image, region, ratio):
    img = np.array(image)
    x0, y0, x1, y1 = region
    img = img[y0:y1, x0:x1]
    Nx, Ny, _ = img.shape
    NNx, NNy = np.floor(Nx*ratio), np.floor(Ny*ratio)
    print NNx, NNy
    # convert i, j (new coordinates) to old coordinates
    
    return Image.fromarray(img)

def crop(image, region):
    img = np.array(image)
    x0, y0, x1, y1 = region
    print region
    Nx, Ny, _ = img.shape
    return Image.fromarray(img[y0:y1, x0:x1])