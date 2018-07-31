import numpy as np
import matplotlib.pyplot as plt
from pfm import ReadMiddlebury2014PfmFile as read_pfm


def item_read(file_name):
    width, height, pixels = read_pfm(file_name)
    data = np.array(pixels, dtype=np.float32)
    data = data.reshape((height, width, len(pixels) / (width * height)))
    return ((np.flipud(data))).copy()


def show2(p1, p2):
    pf1 = item_read(p1)
    pf2 = item_read(p2)
    pf1 = pf1.reshape((540, 960))
    pf2 = pf2.reshape((540, 960))

    plt.subplot(121)
    plt.imshow(pf1, cmap='gray')
    plt.subplot(122) 
    plt.imshow(pf2, cmap='gray')
    plt.show()   

if __name__ == "__main__":
    pfm1 = './ref.pfm'
    pfm2 = './res.pfm'
    show2(pfm1, pfm2)
