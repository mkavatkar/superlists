from django.test import TestCase
from django.core.urlresolvers import resolve, reverse_lazy
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List


# Test class for list creation
class NewListTest(TestCase):
    def test_saving_a_post_request(self):
        self.client.post('/lists/new',
                         data={'item_text': "A new list item"})
        new_item = Item.objects.first()
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        new_List = List.objects.first()
        self.assertRedirects(response,
                             '/lists/%d/' % (new_List.id,))


# List view testcase to display in template
class ListViewTest(TestCase):
    def test_uses_list_template(self):
        List_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (List_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')


# Create your tests here.
class HomepageTest(TestCase):
    def test_root_url_resolves_to_homepage(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_html_render(self):
        request = HttpRequest()
        request1 = HttpRequest()
        response = home_page(request)
        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text':  'A new list item'},
            request=request1
            )
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],
                         '/lists/the-only-list-in-the-world/')


class ListAndItemModelsTest(TestCase):

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
