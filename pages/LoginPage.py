from time import sleep

from core.base_page import BasePage
from utils.overlay_handler import OverlayHandler


class LoginPage(BasePage):

    MY_ACCOUNT = [
        "//div[contains(@class,'my-account--menuItem')]",
        "//span[contains(@class,'comet-icon-myaccount')]"
    ]

    SIGN_IN_BTN = [
        "//a[contains(text(),'Sign in')]",
        "//span[contains(text(),'Sign in')]",
        "//button[contains(@class,'my-account')]"
    ]

    EMAIL = [
        "//input[@type='email']",
        "//input[contains(@id,'email')]",
        "//input[@class='cosmos-input cosmos-input-rtl']"
    ]

    EMAIL_DROP = [
        "//div[@data-popper-placement='bottom-end']",
        ".cosmos-dropdown"
    ]

    PASSWORD = [
        "//input[@type='password']",
        "//input[contains(@id,'password')]"
    ]

    SUBMIT = [
        "//button[contains(text(),'Sign in')]",
        "//button[@type='submit']",
        ".cosmos-btn"
    ]

    def login(self, email, password):
        self.find(self.MY_ACCOUNT).hover()
        self.find(self.SIGN_IN_BTN).click()
        self.find(self.EMAIL).fill(email)
        self.find(self.EMAIL_DROP).click()
        self.find(self.SUBMIT).click()
        self.find(self.PASSWORD).fill(password)
        self.find(self.SUBMIT).click()

        self.page.wait_for_load_state("domcontentloaded")
        OverlayHandler.dismiss_overlays(self.page)
