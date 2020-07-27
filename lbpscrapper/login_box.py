from os.path import join
import numpy as np
from imageio import imread

from lbpscrapper import __data_folder__
from lbpscrapper.tools import element_screenshot_to_numpy


class LoginBox(object):
    offset = (145, 87)

    def __init__(self, element):
        self.element = element

    @property
    def screenshot(self):
        return element_screenshot_to_numpy(self.element)

    def _cut_screenshot(self, im, interspace=48, width=45, offset=(0, 0)):
        imgs = []
        for i in range(4):
            for j in range(4):
                imgs.append(im[i * interspace + offset[0]:i * interspace + width + offset[0],
                            j * interspace + offset[1]:j * interspace + width + offset[1]])
        imgs = np.array(imgs)
        return imgs

    @property
    def numbers_image(self):
        im = imread(join(__data_folder__, "login_box.png"))
        imgs = self._cut_screenshot(im,offset=(0,0))
        res = imgs[[0, 12, 14, 1, 4, -1, 6, 10, 7, 2]]
        return res

    def get_numbers_position(self):
        im = self.screenshot

        imgs = self._cut_screenshot(im, offset=offset)
        mask = self.numbers_image
        err = np.abs(imgs[:, None] - mask[None]).sum((2, 3, 4))
        index = np.argmin(err, axis=1)
        index[imgs.mean((-1)).std((1, 2)) < 10] = -1

        pass
