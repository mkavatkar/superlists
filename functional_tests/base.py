from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import sys
import os


class FunctionalTest(StaticLiveServerTestCase):
    # setup the chrome driver
    def setUp(self):
        self.chromedriver = "/Users/mihirkavatkar/Documents/chromedriver"
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
