import os
import time

from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException, \
    StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class DriverActions:
    def __init__(self, driver):
        self.driver = driver

    def get_wait(self, wait=10):
        return WebDriverWait(self.driver, wait, poll_frequency=1,
                             ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException,
                                                 StaleElementReferenceException])

    def find_element(self, *element):
        return self.driver.find_element(*element)

    def find_elements(self, *element):
        return self.driver.find_elements(*element)

    def browser_back(self):
        self.driver.back()

    def scroll_to_web_element_with_javascript(self, element):
        try:
            self.get_wait(2).until(EC.visibility_of(self.driver.find_element(*element)))
            return True
        except Exception as e:
            print("Element not found, ", e)
            return False

    def click_on_web_element_with_actions_class(self, element):

        actions = ActionChains(self.driver)
        assert self.scroll_to_web_element_with_javascript(element) is True, "Unable to scroll to element"
        try:
            actions.move_to_element(self.get_wait(2)
                                    .until(EC.element_to_be_clickable(element))).click().perform()
            if self.accept_browser_alert():
                print("Alert is present.")
            else:
                print("Alert is absent.")

            return True
        except Exception as e:
            print("Element not found, ", e)
            return False

    def click_on_web_element_with_actions_class_with_offset(self, element, x_offset, y_offset):
        """
        :param element: WebElement click based on offset
        :param element:
        :param x_offset:
        :param y_offset:
        :return:
        """
        actions = ActionChains(self.driver)
        try:
            actions.move_to_element_with_offset(element, x_offset, y_offset).click().perform()
        except Exception as e:
            print("Element not found, ", e)

    def scroll_to_web_element_with_javascript_without_checking_visibility(self, element):
        """
        :param element: WebElement to scroll to element without checking visibility
        :param element:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return True
        except Exception as e:
            print("Element not found, ", e)
            return False

    def mouse_hover_on_web_element_with_actions_class(self, element):
        actions = ActionChains(self.driver)
        try:
            actions.move_to_element(element).perform()
        except Exception as e:
            print("Element not found, ", e)

    @staticmethod
    def select_dropdown_item(element, item_text):
        """
        :param element: WebElement to select dropdown item
        :param element:
        :param item_text: Dropdown item text to select
        :param item_text:
        :return:
        """
        try:
            select = Select(element)
            select.select_by_visible_text(item_text)
            return True
        except Exception as e:
            print("Element not found, ", e)
            return False

    def drag_and_drop_element_with_actions_class(self, source, destination):
        actions = ActionChains(self.driver)
        try:
            actions.drag_and_drop(source, destination).perform()
            return True
        except Exception as e:
            print("Element not found, ", e)
            return False

    def drag_and_drop_web_element_with_javascript(self):
        try:
            self.driver.execute_script("""
            var el = document.getElementById(`${draggable_element_id}`);
            var dt = document.getElementById(`${drop_target_element_id}`);
            dt.appendChild(el);
            """)
            return True
        except Exception as e:
            print("Element not found, ", e)
            return False

    def type_text(self, element, text=''):
        """
        :param element: WebElement to type text
        :param element:
        :param text:
        :return:
        """
        try:
            assert True if self.scroll_to_web_element_with_javascript(element) else "Unable to scroll to element"
            self.get_wait(2).until(EC.visibility_of(self.find_element(*element)))
            el = self.driver.find_element(*element)
            el.send_keys(Keys.CONTROL + "a")
            el.send_keys(Keys.DELETE)
            el.send_keys(text)
            return True

        except Exception as e:
            print("Element not found, ", e)
            return False

    def drag_item(self, element, x_axis, y_axis):
        """
        drag item based to x axis and y axis
        :param element:
        :param x_axis:
        :param y_axis:
        :return:
        """
        try:
            actions = ActionChains(self.driver)
            actions.drag_and_drop_by_offset(element, x_axis, y_axis).perform()
            return True
        except Exception as e:
            print("Element not found, ", e)
            return False

    def accept_browser_alert(self):
        try:
            self.get_wait(1).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
            self.driver.switch_to.default_content()
            return True
        except Exception as e:
            print("No alert was there to accept, ", e)

    def check_url_in_new_tab(self, new_tab_url):
        """
        check url in a new tab
        :param new_tab_url:
        :return:
        """
        try:
            try:
                tabs = self.driver.window_handles
                if len(tabs) > 1:
                    self.driver.switch_to.window(tabs[1])
                if self.driver.get_current_url() != new_tab_url:
                    assert False
                if len(tabs) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(tabs[0])
                else:
                    self.driver.switch_to.window(tabs[0])
                return True
            except Exception as e:
                print("Element not found, ", e)
                return False
        except Exception as e:
            print("Element not found, ", e)
            return False

    def switch_to_browser_tab(self, tab_title):
        """
        switch to browser tab
        :param tab_title:
        :return:
        """
        try:
            tabs = self.driver.window_handles
            for tab in tabs:
                self.driver.switch_to.window(tab)
                print("Current tab title: ", self.driver.title)
                if self.driver.title == tab_title:
                    break
            print("Current url: ", self.driver.get_current_url())
            return True
        except Exception as e:
            print("Element not found, ", e)
            return False

    def wait_until_invisibility_of_element(self, element):
        """
        wait until element is invisible
        :param element:
        :return:
        """
        try:
            self.get_wait().until(EC.invisibility_of_element_located(element))
            return True
        except Exception as e:
            print("Element was gone, ", e)
            return False

    def refresh_page(self):
        """
        Following method refreshes the current page and wait for twenty seconds to load the page
        :return:
        """
        try:
            self.driver.refresh()
            if self.accept_browser_alert():
                print("Alert is present")
                try:
                    self.get_wait(25).until(EC.visibility_of((By.CLASS_NAME, "modal-backdrop")))
                except Exception as e:
                    print(e)
            else:
                print("Alert is not present")
            return True
        except Exception as e:
            print(e)

    def select_web_element_with_control_pressed(self, element_list):
        """
        select web element with control pressed
        :param element_list:
        :return:
        """
        try:
            actions = ActionChains(self.driver)
            for element in element_list:
                assert self.scroll_to_web_element_with_javascript(element), "Unable to scroll to element"
                actions.key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL).perform()

            return True
        except Exception as e:
            print("Element not found, ", e)
            return False

    def press_tab(self, element):
        """
        Press tab key
        :param element:
        :return:
        """
        try:
            self.get_wait(5).until(EC.visibility_of_element_located(element))
            element.send_keys(Keys.TAB)
            return True
        except Exception as e:
            print("Element not found, ", e)
            return False

    def navigate_to_url(self, url):
        """
        Navigate to url
        :param url:
        :return:
        """
        try:
            self.driver.get(url)
            return True
        except Exception as e:
            print(e)

    @staticmethod
    def upload_image(element, image_name):
        """
        This method will take image name age process it to get it's absolute path and then send it to file input
        :param element:
        :param image_name:
        :return:
        """
        try:
            file = os.path.abspath(image_name)
            element.send_keys(file)
            return True
        except Exception as e:
            print(e)

    def click_on_web_element_using_javascript(self, element):
        try:
            self.driver.execute_script("arguments[0].click();", element)
            if self.accept_browser_alert():
                print("Alert is present")
            else:
                print("Alert is not present")
            return True
        except Exception as e:
            print("Element not found, ", e)

    def copy_text_from_element_using_javascript(self, element):
        """
        This method will copy text from element using javascript
        :param element:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].select();", element)
            self.driver.execute_script("document.execCommand('Copy');")
            return True
        except Exception as e:
            print("Element not found, ", e)

    def paste_text_to_element_using_javascript(self, element):
        """
        This method will paste text to element using javascript
        :param element:
        :return:
        """
        try:
            self.driver.execute_script("arguments[0].select();", element)
            self.driver.execute_script("document.execCommand('Paste');")
            return True
        except Exception as e:
            print("Element not found, ", e)

    def switch_to_frame(self, element):
        """
        This method will switch to frame
        :param element:
        :return:
        """
        try:
            self.driver.switch_to.frame(self.driver.find_element(*element))
            return True
        except Exception as e:
            print("Element not found, ", e)
            return False

    def implicit_wait(self, time_in_seconds):
        return self.driver.implicitly_wait(time_in_seconds)

    @staticmethod
    def implicit_wait_time(time_in_seconds):
        return time.sleep(time_in_seconds)

    def explicit_wait(self, time_in_seconds, element):
        try:
            return self.get_wait(time_in_seconds).until(EC.visibility_of(element))
        except Exception as e:
            print("Element not found, ", e)

    # scroll page to amount of pages
    def scroll_page_to_amount(self, amount):
        self.driver.execute_script("window.scrollBy(0, " + str(amount) + ");")

    def check_tab_title(self, title):
        """
        This method will check tab title
        :param title:
        :return:
        """
        try:
            driver_title = self.driver.title
            return driver_title == title
        except Exception as e:
            print("Title not found, ", e)
            return False

    def get_attribute_value(self, element, attribute):
        """
        This method will get attribute
        :param element:
        :param attribute:
        :return:
        """
        try:
            return self.find_element(*element).get_attribute(attribute)
        except Exception as e:
            print("Attribute not found, ", e)
            return False

    def get_element_text(self, element):
        """
        This method will get element text
        :param element:
        :return:
        """
        try:
            return self.get_wait().until(EC.visibility_of_element_located(element)).text
        except Exception as e:
            print("Text not found, ", e)
