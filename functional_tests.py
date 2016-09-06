import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         "Enter a To-Do item")

        inputbox.send_keys('Buy a dog')
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('item_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == 'Buy a dog' for row in rows),
            "New to-do item did not appear in table"
        )

        self.fail("Finished the test!")


if __name__ == '__main__':
    unittest.main()
