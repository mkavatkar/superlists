from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_empty_list_of_items(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk\n')
        self.check_if_row_exists_in_list_table('1: Buy milk')

        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        self.check_if_row_exists_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        self.browser.find_element_by_id('id_new_item').send_keys('Make tea\n')
        self.check_if_row_exists_in_list_table('1: Buy milk')
        self.check_if_row_exists_in_list_table('2: Make tea')
