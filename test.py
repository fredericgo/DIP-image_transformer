#test
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from scipy import interpolate

def BicubicInterpolator(p):
    if p.size != 48: 
        return lambda x, y: np.array(255)

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


    def interpolator(xnew, ynew):
        x = xnew
        y = ynew
        
        x2 = x * x
        x3 = x2 * x
        y2 = y * y
        y3 = y2 * y

        f =  (a00 + a01 * y + a02 * y2 + a03 * y3) +\
               (a10 + a11 * y + a12 * y2 + a13 * y3) * x +\
               (a20 + a21 * y + a22 * y2 + a23 * y3) * x2 +\
               (a30 + a31 * y + a32 * y2 + a33 * y3) * x3

        return np.clip(f, 0, 255)

    return interpolator


image = Image.open("logo.jpeg")
img = np.array(image)

h, w, _ = img.shape
print "width, height: ", w, h

x, y = np.arange(h), np.arange(w)
print x.shape, y.shape

i, j = 8, 7
xnew, ynew = i, j
rot = 5 * np.pi / 180
xnew = np.cos(rot) * i + np.sin(rot) * j
ynew = -np.sin(rot) * i + np.cos(rot) * j

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

print xnew, ynew
print xmin, xmax
print ymin, ymax

grid_x, grid_y = np.mgrid[0:1:100j, 0:1:100j]
neighbors = img[xmin:xmax, ymin:ymax]

print img[:,:, 0]
print neighbors



def show():
    coords = [[i,j] for i in x for j in y]
    new_img = np.zeros_like(img)
    for i, j in coords:
        xnew = np.cos(rot) * i + np.sin(rot) * j
        ynew = -np.sin(rot) * i + np.cos(rot) * j
        if xnew < 0 or w - xnew < 2 or ynew < 0 or h - ynew < 2:
            new_img[i,j] = 255
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

            
            #if xmin < 0 or xmax > w or ymin < 0 or ymax > h:
            #    new_img[i, j] = 0
            #    continue
            neighbors = img[xmin:xmax, ymin:ymax].astype(np.float64)
            new_img[i, j] = BicubicInterpolator(neighbors)(xnew-int(xnew), ynew-int(ynew))
            
    plt.imshow(new_img)
    plt.show()



show()

