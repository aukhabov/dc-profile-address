from selenium.webdriver.common.by import By

from extensions import get_driver, highlight_element, scroll_to_element


class BasePage:

    def __init__(self, url="/"):
        self.driver = get_driver()
        self.driver.get(f"https://www.delivery-club.ru{url}")

    def highlight_select(self, selector):
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        scroll_to_element(element)
        highlight_element(element)
        return element

    def page_refresh(self):
        self.driver.refresh()
