from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Testcase class
class NewVisitorTest(FunctionalTest):

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
