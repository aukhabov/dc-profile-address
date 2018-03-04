from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver_instance = None


def get_driver():
    global driver_instance
    if not driver_instance:
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver_instance = webdriver.Chrome(chrome_options=chrome_options)
        driver_instance.implicitly_wait(0.5)
    return driver_instance


def driver_quit():
    global driver_instance
    if driver_instance:
        driver_instance.quit()
        driver_instance = None


def scroll_to_element(element):
    get_driver().execute_script("arguments[0].scrollIntoView(true);", element)


def highlight_element(element):
    driver = get_driver()
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, "color: red; border: 1px solid red;")
    sleep(0.5)
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, "")


def wait_for_element(selector=None, timeout=3, option="presence"):
    if option == "presence":
        return WebDriverWait(get_driver(), timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    elif option == "clickable":
        return WebDriverWait(get_driver(), timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
    elif option == "alert":
        return WebDriverWait(get_driver(), timeout).until(EC.alert_is_present())
    elif option == "iframe":
        WebDriverWait(get_driver(), timeout).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, selector)))
    else:
        return WebDriverWait(get_driver(), timeout).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, selector), option))

