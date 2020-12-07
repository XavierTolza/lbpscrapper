from os.path import join

import numpy as np
from imageio import imread
from selenium.common.exceptions import NoSuchElementException

from lbpscrapper import __data_folder__
from lbpscrapper.tools import element_screenshot_to_numpy


class LoginBox(object):
    offset = (145, 87)
    interspace = 48

    def __init__(self, driver, element, buttons_screenshot_kwargs: dict = {}):
        self.buttons_screenshot_kwargs = buttons_screenshot_kwargs
        self.driver = driver
        self.element = element

    @property
    def screenshot(self):
        return element_screenshot_to_numpy(self.element)

    def _cut_screenshot(self, im, interspace=None, width=45, offset=None):
        if offset is None:
            offset = self.offset
        if interspace is None:
            interspace = self.interspace
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
        imgs = self._cut_screenshot(im, offset=(0, 0))
        res = imgs[[0, 12, 14, 1, 4, -1, 6, 10, 7, 2]]
        return res

    def get_button_screenshot(self, button_index):
        with self.get_into_iframe:
            return element_screenshot_to_numpy(self.driver.find_element_by_id("val_cel_%i" % button_index))

    def get_buttons_screenshot(self, offset_x=46, offset_y=7, size_x=45, size_y=45, margin_x=3, margin_y=3, N_x=4,
                               N_y=4):
        full_x = size_x + margin_x
        full_y = size_y + margin_y
        stop_x = offset_x + full_x * N_x
        stop_y = offset_y + full_x * N_y
        # imgs = np.array([self.get_button_screenshot(i) for i in range(16)])
        # return imgs
        with self.get_into_iframe:
            img = element_screenshot_to_numpy(self.driver.find_element_by_id("blocImage"))
            padding = np.ones((stop_y - img.shape[0],) + img.shape[1:], dtype=np.uint8) * 255
            img = np.concatenate([img, padding], axis=0)
            img_cut = img[offset_y:stop_y, offset_x:stop_x]
            img_reshaped = img_cut.reshape((N_y, full_y, N_x, full_x, -1))
            img_reshaped_cut = img_reshaped[:, :size_y, :, :size_x]
        return np.moveaxis(img_reshaped_cut, 2, 1)

    def get_numbers_position(self):
        mask = self.numbers_image.mean(-1)
        imgs = self.get_buttons_screenshot(**self.buttons_screenshot_kwargs).mean(-1)
        imgs = imgs.reshape((4 * 4,) + mask.shape[-2:])
        err = np.abs(imgs[:, None] - mask[None]).sum((2, 3))
        index = np.argmin(err, axis=1)

        index[imgs[:, 2:-2, 2:-2].std((1, 2)) < 10] = -1

        res = np.sum((np.arange(10)[:, None] == index[None, :]) * np.arange(16)[None, :], axis=1)
        return res

    @property
    def get_into_iframe(self):
        return self.driver.get_into_iframe(self.element)

    def click_on_button(self, button_index):
        with self.get_into_iframe:
            self.driver.find_element_by_id("val_cel_%i" % button_index).click()

    def enter_login(self, login):
        with self.get_into_iframe:
            self.driver.find_element_by_id("val_cel_identifiant").send_keys(login)

    def enter_code(self, code):
        pos = self.get_numbers_position()
        for char in code:
            charpos = pos[int(char)]
            self.driver.debug("Clicking on login button %s on pos %i" % (char, charpos))
            self.click_on_button(charpos)

    @property
    def is_ready(self):
        with self.get_into_iframe:
            try:
                self.driver.find_element_by_id("val_cel_0")
                res = True
            except NoSuchElementException:
                res = False
            return res

    def validate(self):
        self.driver.switch_to.frame(self.element)
        self.driver.find_element_by_id("valider").click()
        self.driver.switch_to.default_content()
        return
