import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


# Testcase class
class NewVisitorTest(StaticLiveServerTestCase):

    # setup the chrome driver
    def setUp(self):
        self.chromedriver = "/usr/local/bin/chromedriver/chromedriver"
        os.environ["webdriver.chrome.driver"] = self.chromedriver
        self.browser = webdriver.Chrome(self.chromedriver)
        self.browser.implicitly_wait(3)

    # Driver quit function
    def tearDown(self):
        self.browser.quit()

    def check_if_row_exists_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_layout_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512, delta=5
        )
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
            )

    def test_can_start_a_list_and_retrieve_later(self):
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         "Enter a to-do item")

        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        edith_current_url = self.browser.current_url
        # import time
        # time.sleep(10)
        self.assertRegex(edith_current_url, '/lists/.+')
        self.check_if_row_exists_in_list_table('1: Buy peacock feathers')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # import time
        # time.sleep(10)
        self.check_if_row_exists_in_list_table(
            '2: Use peacock feathers to make a fly')
        self.check_if_row_exists_in_list_table('1: Buy peacock feathers')

        self.browser.quit()
        self.browser = webdriver.Chrome(self.chromedriver)

        # login 1
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # login 1 entering its own list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # login 1 gets its own url
        francis_current_url = self.browser.current_url
        self.assertRegex(francis_current_url, '/lists/.+')
        self.assertNotEqual(francis_current_url, edith_current_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
