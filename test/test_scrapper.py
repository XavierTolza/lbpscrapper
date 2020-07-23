from unittest import TestCase

from lbpscrapper.scrapper import LBP


class TestLBP(TestCase):
    def test_001(self):
        with LBP("toto", 5496, headless=False) as s:
            s.login()
            pass
