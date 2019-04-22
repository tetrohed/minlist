import os
import time
import unittest

from testing.base import FunctionalTestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


class ListItemValidationTestCase(FunctionalTestCase):
    
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url + '/lists')

        input_box = self.get_item_input_box()

        input_box.send_keys('')
        input_box.send_keys(Keys.ENTER)

        self.wait_for(lambda: 
            self.browser.find_element_by_css_selector('#id_text:invalid'))

        self.get_item_input_box().send_keys('Buy something for the kids birthday')
        self.wait_for(lambda: 
            self.browser.find_elements_by_css_selector('#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy something for the kids birthday')

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: 
            self.browser.find_elements_by_css_selector('#id_text:invalid'))

        self.get_item_input_box().send_keys('Buy something else for the kids birthday')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('2: Buy something else for the kids birthday')

    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url + '/lists')

        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')

        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text, 
            "you've already got this in your list"))

