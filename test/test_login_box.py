from os.path import join, dirname, abspath
from unittest import TestCase

import numpy as np
from imageio import imread

from lbpscrapper.login_box import LoginBox as _LoginBox


class LoginBox(_LoginBox):
    @property
    def screenshot(self):
        return imread(join(dirname(abspath(__file__)), "login_box.png"))


class TestLoginBox(TestCase):
    def test_numbers_image(self):
        lb = LoginBox(None)
        assert lb.numbers_image is not None

    def test_get_numbers_position(self):
        lb = LoginBox(None)
        res = lb.get_numbers_position()
        assert np.all(res == [0, 12, 14, 1, 4, 15, 6, 10, 7, 2])
