import numpy as np
from scipy.interpolate import RectBivariateSpline
from scipy.ndimage.interpolation import zoom as _zoom
from itertools import product
from PIL import Image

def nn_interpolation(u, v, img):
    i, j = int(u + 0.5) - 1, int(v + 0.5) - 1
    return img[j, i]


def biliear_interpolation(u, v, img):
    if u > int(u): 
        x0 = int(u)
        x1 = int(u) + 1
    else:
        x0 = int(u)
        x1 = int(u)
    if v > int(v):
        y0 = int(v)
        y1 = int(v) + 1
    else:
        y0 = int(v)
        y1 = int(v)
    if y1 > img.shape[0]: y1 -= 1
    if x1 > img.shape[1]: x1 -= 1

    f00 = img[y0, x0].astype(float)
    f10 = img[y1, x0].astype(float)
    f01 = img[y0, x1].astype(float)
    f11 = img[y1, x1].astype(float)

    dx, dy = u - x0, v - y0
    
    f = f00 + (f01 - f00) * dx 
    f += (f10 - f00) * dy 
    f += (f11 + f00 - f10 - f01) * dx * dy
    return f
    

def interpolation_mothods(m, img):
    f = {'nearest neighbor' : nn_interpolation,
         'bilinear': biliear_interpolation}
    return lambda x, y : f[m](x, y, img)


def toArray(image):
    return np.array(image)


def transform(image):
    return image

def zoom(image, region, ratio, interpolation='bilinear'):

    img = np.array(image)

    size = img.shape
    x0, y0, x1, y1 = region
    if x1 > size[1]: 
        x1 = size[1]
    if y1 > size[0]: 
        y1 = size[0]
    if x1 < 0: 
        x1 = 0
    if y1 < 0: 
        y1 = 0
    #img = img[y0:y1, x0:x1]
    
    Ny, Nx = int(y1 - y0), int(x1 - x0)
    #Nx, Ny, _ = img.shape
    NNx, NNy = round(Nx*ratio), round(Ny*ratio)
    print "original: ", Nx, Ny
    print "new: ", NNx, NNy

    new_img = np.empty((NNy, NNx, 3))

    # convert i, j (new coordinates) to old coordinates

    if interpolation != "bicubic":
        interpolate = interpolation_mothods(interpolation, img)
        for i in range(int(NNx)):
            for j in range(int(NNy)):
                new_img[j, i] = interpolate(x0 + i / ratio, y0 + j / ratio)
    else:
        img = img[y0:y1, x0:x1]

        new_img[:,:,0] = _zoom(img[:,:,0], ratio, order=1)
        new_img[:,:,1] = _zoom(img[:,:,1], ratio, order=1)
        new_img[:,:,2] = _zoom(img[:,:,2], ratio, order=1)

    return Image.fromarray(new_img.astype(np.uint8))

def crop(image, region):
    img = np.array(image)
    x0, y0, x1, y1 = region
    print region
    Nx, Ny, _ = img.shape
    return Image.fromarray(img[y0:y1, x0:x1])


