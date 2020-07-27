from os.path import join, dirname, abspath
from unittest import TestCase

from imageio import imread
from lbpscrapper import __data_folder__

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
        lb.get_numbers_position()
