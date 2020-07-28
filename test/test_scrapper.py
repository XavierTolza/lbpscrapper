import os
from unittest import TestCase

from lbpscrapper.scrapper import LBP


class TestLBP(TestCase):
    def test_001(self):
        user = os.getenv("USER")
        passw = os.getenv("PASS")
        with LBP(user, passw, headless=False) as s:
            s.login()
            pass
