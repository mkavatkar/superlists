from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_empty_list_of_items(self):
        self.fail('write me!')
