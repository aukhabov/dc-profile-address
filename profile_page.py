from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from base_page import BasePage
from extensions import wait_for_element


class ProfilePage(BasePage):

    def __init__(self):
        super().__init__("/profile")
        self._address_input_field = "#user-addr__input"
        self._suggest_list = ".ui-menu-item"
        self._yandex_map_button = ".user-addr__links-item"
        self._submit_address_button = ".user-addr__submit"
        self._delete_address_button = ".delete_uaddress"
        self._user_addresses = ".addresses"
        self._discount_widget = "#fl-52618"
        self._discount_notification_allow = ".Notification-buttonAllow"

        self._yamap_popup = "#map"
        self._yamap_zoom_in = ".ymaps-2-1-60-zoom__plus"
        self._yamap_zoom_out = ".ymaps-2-1-60-zoom__minus"
        self._yamap_confirm_button = "#confirm_addr"
        self._yamap_close_button = ".user-addr__popup__close"
        try:
            self.close_overlay_widget()
        except TimeoutException:
            pass

    def fill_address_form(self, address):
        self.highlight_select(self._address_input_field).send_keys(address)

    def add_manual_address(self, address):
        self.fill_address_form(address)
        new_address = self.highlight_select(self._address_input_field).text
        self.highlight_select(self._submit_address_button).click()
        wait_for_element(self._user_addresses, option=new_address)
        return new_address

    def add_address_from_suggest(self, address):
        self.fill_address_form(address)
        wait_for_element(self._suggest_list)
        self.highlight_select(self._suggest_list)
        new_address = self.highlight_select(self._address_input_field).text
        self.highlight_select(self._submit_address_button).click()
        wait_for_element(self._user_addresses, option=new_address)
        return new_address

    def add_address_from_yamap(self):
        self.highlight_select(self._yandex_map_button).click()
        wait_for_element(self._yamap_confirm_button, timeout=10, option="clickable").click()
        sleep(3)
        new_address = self.highlight_select(self._address_input_field).text
        self.driver.find_element(By.CSS_SELECTOR, self._submit_address_button).click()
        wait_for_element(self._user_addresses, option=new_address)
        return new_address

    def table_with_addresses(self):
        return self.driver.find_elements(By.CSS_SELECTOR, self._user_addresses)

    def delete_address(self, index):
        address = self.table_with_addresses()[index]
        address.find_element(By.CSS_SELECTOR, self._delete_address_button).click()
        wait_for_element(option="alert").accept()

    def address_list(self):
        return [address.text for address in self.table_with_addresses()]

    def yamap_zoom(self, zoom_style):
        self.highlight_select(self._yandex_map_button).click()
        wait_for_element(self._yamap_confirm_button, timeout=10, option="clickable")
        try:
            if zoom_style == "in":
                selector = self._yamap_zoom_in
            else:
                selector = self._yamap_zoom_out
            wait_for_element(selector, option="clickable")
            return True
        except TimeoutException:
            return

    def yamap_close(self):
        self.highlight_select(self._yandex_map_button).click()
        wait_for_element(self._yamap_close_button, option="clickable").click()
        try:
            self.highlight_select(self._yamap_popup)
        except NoSuchElementException:
            return True

    def close_overlay_widget(self):
        main_window = self.driver.current_window_handle
        wait_for_element(self._discount_widget, timeout=10, option="iframe")
        self.highlight_select(self._discount_notification_allow).click()
        self.driver.switch_to.window(main_window)
