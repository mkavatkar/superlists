from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError


class ListAndItemModelsTest(TestCase):
    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first item of this list'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item of this list'
        second_item.list = list_
        second_item.save()

        save_list = List.objects.first()
        self.assertEqual(save_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, 'The first item of this list')
        self.assertEqual(saved_items[0].list, list_)

        self.assertEqual(saved_items[1].text, 'The second item of this list')
        self.assertEqual(saved_items[1].list, list_)
