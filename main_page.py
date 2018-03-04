from base_page import BasePage
from extensions import wait_for_element


user_login = ""
user_password = ""


class MainPage(BasePage):

    def __init__(self):
        super().__init__()
        self._login_button = ".authorization-btn--enter"
        self._email_input_field = ".user-login__input"
        self._password_input_field = ".user-login__input[type=password]"
        self._authorization_form_submit = ".user-login__btn--submit"
        self._profile_button = "#user-profile"

    def authorization(self):
        self.highlight_select(self._login_button).click()
        self.highlight_select(self._email_input_field).send_keys(user_login)
        self.highlight_select(self._password_input_field).send_keys(user_password)
        self.highlight_select(self._authorization_form_submit).click()
        wait_for_element(self._profile_button)
