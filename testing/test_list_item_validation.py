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

        input_box = self.browser.find_element_by_id('id_new_item')

        input_box.send_keys('')
        input_box.send_keys(Keys.ENTER)

        self.wait_for(lambda: 
            self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
                "You can't have an empty list item"))

        self.browser.find_element_by_id('id_new_item').send_keys('Buy something for the kids birthday')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy something for the kids birthday')

        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for(lambda: 
            self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
                "You can't have an empty list item"))

        self.browser.find_element_by_id('id_new_item').send_keys('Buy something for the kids birthday')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy somehting for the kids birthday')

        

