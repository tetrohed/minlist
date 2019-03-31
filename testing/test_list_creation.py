import os
import time
import unittest

from testing.base import FunctionalTestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


class ListCreationTestCase(FunctionalTestCase):

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url + '/lists')
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'),'Enter a to-do item')

        input_box.send_keys('buy a tdd book and learn about django')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: buy a tdd book and learn about django')

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('just try javascript and you will learn it')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('2: just try javascript and you will learn it')

        self.check_for_row_in_list_table('1: buy a tdd book and learn about django')
        self.check_for_row_in_list_table('2: just try javascript and you will learn it')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url + '/lists')
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('call amy')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: call amy')

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Chrome()

        self.browser.get(self.live_server_url + '/lists')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('call amy', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: buy milk')

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, 'lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('call amy', page_text)
        self.assertIn('buy milk', page_text)
