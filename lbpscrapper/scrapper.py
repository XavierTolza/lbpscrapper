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
            self.wait_for_css_element("#verifStatAccount")
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
            _, name, number = account.find_element_by_css_selector("div.title").text.split(",")
            number = int(number.replace('N°', ''))
            amount = float(account.find_element_by_css_selector(".amount").text.split(" ")[0])
            accounts.append(dict(name=name, number=number, amount=amount))
        return accounts
