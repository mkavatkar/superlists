import os
from selenium import webdriver
import unittest


# Testcase class
class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.chromedriver = "/Users/mihirkavatkar/Documents/chromedriver"
        os.environ["webdriver.chrome.driver"] = self.chromedriver
        self.browser = webdriver.Chrome(self.chromedriver)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_later(self):
        self.browser.get("http://127.0.0.1:8000/")
        self.assertIn('To-Do', self.browser.title)
        self.fail("Finished the test!")


if __name__ == '__main__':
    unittest.main()
