from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
import time
import unittest


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.MAX_WAIT = 3
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return 
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(.5)

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
        self.assertNotIn(page_text, 'call amy')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('buy milk')

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, 'lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(page_text, 'call amy')
        self.assertIn(page_text, 'buy milk')