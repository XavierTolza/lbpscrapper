import re
from glob import glob
from os.path import join
from time import sleep

from selenium.common.exceptions import NoSuchElementException

from easyscrapper.firefox import Firefox
from lbpscrapper.login_box import LoginBox


class LBP(Firefox):
    base_url = "https://www.labanquepostale.fr/"

    def __init__(self, username, password, *args, **kwargs):
        super(LBP, self).__init__(*args, **kwargs)
        self.username = str(username)
        self.password = str(password)

    def login(self):
        self.get(self.base_url)
        while not self.connected:
            while not self.login_window_visible:
                self.button_connect.click()
                sleep(1)
            lb = self.login_box
            while not lb.is_ready:
                sleep(0.5)
            lb.enter_login(self.username)
            lb.enter_code(self.password)
            lb.validate()
            self.wait_for_css_element("i.icon-user")
            pass

    @property
    def button_connect(self):
        res = None
        try:
            res = self.find_element_by_id("verifStatAccount")
        except NoSuchElementException:
            pass
        return res

    @property
    def login_window_visible(self):
        return self.find_element_by_css_selector("div.navmain-account").is_displayed()

    @property
    def connected(self):
        but = self.button_connect
        if but is None:
            return True
        return not (but.text == "ME CONNECTER")

    @property
    def login_box(self):
        res = self.find_element_by_css_selector("div.iframe iframe")
        return LoginBox(self, res)

    def go_to_e_releves(self):
        button_css = "div.stripe-footer ul li a"
        self.wait_for_css_element(button_css)
        while self.css_element_exists(button_css):
            self.find_elements_by_css_selector(button_css)[3].click()
        self.wait_for_css_element("a.collapse__toggle.fix")
        for el in self.find_elements_by_css_selector("a.collapse__toggle.fix"):
            el.click()

    @property
    def ereleves(self):
        elements = self.find_elements_by_css_selector("ul.mbm.liste-cpte li a")
        res = [dict(date=i.find_element_by_class_name("date").text,
                    name=i.find_element_by_css_selector("span").text,
                    element=i) for i in elements]
        return res

    def parse_accounts(self):
        accounts = []
        for account in self.find_elements_by_css_selector(
                "#main ul.listeDesCartouches li div.account-resume2 div.stripe"):
            _, name, number = account.find_element_by_css_selector("div.title").text.split("\n")
            number = number.replace('N°', '')
            amount = float("".join(account.find_element_by_css_selector(".amount")
                                   .text.split(" ")[:-1]).replace(",", "."))
            accounts.append(dict(name=name, number=number, amount=amount))
        return accounts

    def file_glob_exists(self, file_glob):
        matching_files = list(glob(file_glob))
        file_exists = len(matching_files) > 0
        return file_exists, matching_files

    def download_releve_if_not_downloaded(self, releve, accounts):
        date = releve["date"]
        month, year = date.split("/")

        # Find account number
        account_name = re.match("RELEVÉ (.+) (CCP )?[0-9/]", releve["name"]).group(1)
        for account in accounts:
            if account["name"] in account_name:
                account_number = account["number"]
                break

        # Search for filename
        filename_glob = join(self.download_dir, f'releve_CCP{account_number}_{year}{month}*.pdf')

        if not self.file_glob_exists(filename_glob)[0]:
            releve["element"].click()

        while not self.file_glob_exists(filename_glob)[0]:
            sleep(0.5)

        res = self.file_glob_exists(filename_glob)[1]
        return res
