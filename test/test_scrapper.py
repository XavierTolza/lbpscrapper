import os
from time import sleep
from unittest import TestCase

from lbpscrapper.scrapper import LBP


class TestLBP(TestCase):
    def test_001(self):
        user = os.getenv("USER")
        passw = os.getenv("PASS")
        with LBP(user, passw, headless=False) as s:
            s.login()
            sleep(1)
            s.go_to_e_releves()
            releves = s.ereleves
            pass
