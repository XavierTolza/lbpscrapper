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
            accounts = s.parse_accounts()
            s.go_to_e_releves()
            releves = s.ereleves
            for r in releves:
                s.download_releve_if_not_downloaded(r, accounts)
            return
