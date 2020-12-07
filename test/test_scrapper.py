import os
from time import sleep
from unittest import TestCase

from lbpscrapper.scrapper import LBPChromium, LBPFirefox


class TestLBP(TestCase):
    def test_chromium(self, cls=LBPChromium):
        user = os.getenv("USER")
        passw = os.getenv("PASS")
        with cls(user, passw, headless=False, download_dir="C:\\Users\\Xavier\\Downloads") as s:
            s.login()
            sleep(1)
            accounts = s.parse_accounts()
            s.go_to_e_releves()
            releves = s.ereleves
            for r in releves:
                s.download_releve_if_not_downloaded(r, accounts)
            return

    def test_firefox(self):
        self.test_chromium(LBPFirefox)
