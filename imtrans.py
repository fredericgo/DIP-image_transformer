import numpy as np
from scipy import interpolate
from scipy.ndimage.interpolation import rotate as _rotate

from itertools import product
from PIL import Image

def NNInterpolator(block):
    def interpolator(x, y):
        if block.size == 0: return np.array([255])
        i, j = int(x + 0.5), int(y + 0.5)
        return block[i, j]
    return interpolator


def BilinearInterpolator(block):
    f00 = block[0, 0].astype(float)
    f10 = block[1, 0].astype(float)
    f01 = block[0, 1].astype(float)
    f11 = block[1, 1].astype(float)

    def interpolator(x, y):
        f = f00 + (f01 - f00) * y
        f += (f10 - f00) * x 
        f += (f11 + f00 - f10 - f01) * x * y
        return f
    return interpolator

def BicubicInterpolator(p):
    if p.size != 48: 
        return lambda x, y: np.array(255)

    # from neighbors to coefficients 
    # http://www.paulinternet.nl/?page=bicubic
    a00 = p[1,1]
    a01 = -.5*p[1,0] + .5*p[1, 2];
    a02 = p[1, 0] - 2.5 * p[1, 1] + 2 * p[1, 2] - .5 * p[1, 3];
    a03 = -.5*p[1, 0] + 1.5*p[1, 1] - 1.5*p[1, 2] + .5*p[1,3];
    a10 = -.5*p[0,1] + .5*p[2,1];
    a11 = .25*p[0,0] - .25*p[0,2] - .25*p[2,0] + .25*p[2,2];
    a12 = -.5*p[0,0] + 1.25*p[0,1] - p[0,2] + .25*p[0,3] + .5*p[2,0] - 1.25*p[2,1] + p[2,2] - .25*p[2,3];
    a13 = .25*p[0,0] - .75*p[0,1] + .75*p[0,2] - .25*p[0,3] - .25*p[2,0] + .75*p[2,1] - .75*p[2,2] + .25*p[2,3];
    a20 = p[0,1] - 2.5*p[1,1] + 2*p[2,1] - .5*p[3,1];
    a21 = -.5*p[0,0] + .5*p[0,2] + 1.25*p[1,0] - 1.25*p[1,2] - p[2,0] + p[2,2] + .25*p[3,0] - .25*p[3,2];
    a22 = p[0,0] - 2.5*p[0,1] + 2*p[0,2] - .5*p[0,3] - 2.5*p[1,0] + 6.25*p[1,1] - 5*p[1,2] + 1.25*p[1,3] + 2*p[2,0] - 5*p[2,1] + 4*p[2,2] - p[2,3] - .5*p[3,0] + 1.25*p[3,1] - p[3,2] + .25*p[3,3];
    a23 = -.5*p[0,0] + 1.5*p[0,1] - 1.5*p[0,2] + .5*p[0,3] + 1.25*p[1,0] - 3.75*p[1,1] + 3.75*p[1,2] - 1.25*p[1,3] - p[2,0] + 3*p[2,1] - 3*p[2,2] + p[2,3] + .25*p[3,0] - .75*p[3,1] + .75*p[3,2] - .25*p[3,3];
    a30 = -.5*p[0,1] + 1.5*p[1,1] - 1.5*p[2,1] + .5*p[3,1];
    a31 = .25*p[0,0] - .25*p[0,2] - .75*p[1,0] + .75*p[1,2] + .75*p[2,0] - .75*p[2,2] - .25*p[3,0] + .25*p[3,2];
    a32 = -.5*p[0,0] + 1.25*p[0,1] - p[0,2] + .25*p[0,3] + 1.5*p[1,0] - 3.75*p[1,1] + 3*p[1,2] - .75*p[1,3] - 1.5*p[2,0] + 3.75*p[2,1] - 3*p[2,2] + .75*p[2,3] + .5*p[3,0] - 1.25*p[3,1] + p[3,2] - .25*p[3,3];
    a33 = .25*p[0,0] - .75*p[0,1] + .75*p[0,2] - .25*p[0,3] - .75*p[1,0] + 2.25*p[1,1] - 2.25*p[1,2] + .75*p[1,3] + .75*p[2,0] - 2.25*p[2,1] + 2.25*p[2,2] - .75*p[2,3] - .25*p[3,0] + .75*p[3,1] - .75*p[3,2] + .25*p[3,3];

    def interpolator(x, y):
        x2 = x * x
        x3 = x2 * x
        y2 = y * y
        y3 = y2 * y

        f = (a00 + a01 * y + a02 * y2 + a03 * y3) +\
               (a10 + a11 * y + a12 * y2 + a13 * y3) * x +\
               (a20 + a21 * y + a22 * y2 + a23 * y3) * x2 +\
               (a30 + a31 * y + a32 * y2 + a33 * y3) * x3
        return np.clip(f, 0, 255)
    return interpolator


def zoom(image, region, ratio, method='bilinear'):

    img = np.array(image)

    x0, y0, x1, y1 = region
    img = img[y0:y1, x0:x1]

    w = int(x1 - x0)
    h = int(y1 - y0)

    NNy, NNx = round(h * ratio), round(w * ratio)

    new_img = np.empty((NNy, NNx, 3))
    print new_img.shape
    x = np.arange(NNx)
    y = np.arange(NNy)

    coords = [[i,j] for i in y for j in x]

    interpolator = {
        "nearest neighbor": NNInterpolator,
        "bilinear": BilinearInterpolator, 
        "bicubic": BicubicInterpolator
    }
    
    for i, j in coords:
        ynew = i / ratio
        xnew = j / ratio
        
        if method != "bicubic":
            xmin, xmax = int(xnew), int(xnew) + 2
            ymin, ymax = int(ynew), int(ynew) + 2
        else:
            xmin, xmax = int(xnew) - 2, int(xnew) + 2
            ymin, ymax = int(ynew) - 2, int(ynew) + 2

        if xmin < 0 or xmax > w or ymin < 0 or ymax > h:
            new_img[i, j] = 0
            continue
        else:
            # do interpolation here
            neighbors = img[ymin:ymax, xmin:xmax].astype(np.float64)
            new_img[i, j] = interpolator[method](neighbors)(ynew-int(ynew), xnew-int(xnew))
    # numpy will do somthing nasty: if over 255, the value becomes negative ><
    new_img = np.clip(new_img, 0, 255)
    image = Image.fromarray(new_img.astype(np.uint8))
    image.save("zoom"+method + ".jpg", "jpeg")
    return image

def rotate(image, angle, method="bicubic"):
    interpolator = {
        "nearest neighbor": NNInterpolator,
        "bilinear": BilinearInterpolator, 
        "bicubic": BicubicInterpolator
    }

    img = np.array(image)
    new_img = np.empty_like(img)

    w, h, _ = img.shape
    x = np.arange(w)
    y = np.arange(h)
    
    coords = [[i,j] for i in x for j in y]
    rot = np.pi * angle / 180

    for i, j in coords:
            xnew = np.cos(rot) * i + np.sin(rot) * j
            ynew = -np.sin(rot) * i + np.cos(rot) * j
            if xnew < 0 or w - xnew < 2 or ynew < 0 or h - ynew < 2:
                new_img[i,j] = 255
            else:
                if method != "bicubic":
                    xmin, xmax = int(xnew), int(xnew) + 2
                    ymin, ymax = int(ynew), int(ynew) + 2
                else:
                    xmin, xmax = int(xnew) - 1, int(xnew) + 3
                    ymin, ymax = int(ynew) - 1, int(ynew) + 3
                    if xnew < 2:
                        xmin = xnew
                    if w - xnew < 2 :
                        xmax = xnew
                    if ynew < 2:
                        ymin = ymax
                    if h - ynew < 2:
                        ymax = ynew

                neighbors = img[xmin:xmax, ymin:ymax].astype(np.float64)
                new_img[i, j] = interpolator[method](neighbors)(xnew-int(xnew), ynew-int(ynew))
    image = Image.fromarray(new_img.astype(np.uint8))
    image.save("rotate"+method + ".jpg", "jpeg")
    return image


