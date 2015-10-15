#test
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from scipy import interpolate

image = Image.open("kathmandu2.jpg")
img = np.array(image)

h, w, _ = img.shape
print "width, height: ", w, h

n = 60
x, y = np.arange(h), np.arange(w)
print x.shape, y.shape

interpolate.griddata(x, y, img[:, :, 2])

plt.figure()
plt.show()
