from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item


# Test class for list creation
class NewListTest(TestCase):
    def test_saving_a_post(self):
        self.client.post(
            '/list/new',
            data='item_text': 'A new list item')
        

# List view testcase to display in template
class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')


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

    def test_homepage_to_save_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

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

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The item of this list'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item of this list'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, 'The item of this list')
        self.assertEqual(saved_items[1].text, 'The second item of this list')
