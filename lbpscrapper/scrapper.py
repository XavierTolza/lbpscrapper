from time import sleep

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
        if not self.connected:
            while not self.login_window_visible:
                self.button_connect.click()
                sleep(1)
            lb = self.login_box
            while not lb.is_ready:
                sleep(0.5)
            lb.enter_login(self.username)
            lb.enter_code(self.password)
            lb.validate()
            pass

    @property
    def button_connect(self):
        return self.find_element_by_id("verifStatAccount")

    @property
    def login_window_visible(self):
        return self.find_element_by_css_selector("div.navmain-account").is_displayed()

    @property
    def connected(self):
        return not (self.button_connect.text == "ME CONNECTER")

    @property
    def login_box(self):
        res = self.find_element_by_css_selector("div.iframe iframe")
        return LoginBox(self, res)
