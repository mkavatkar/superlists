from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string


# Create your tests here.
class HomepageTest(TestCase):
    def test_root_url_resolves_to_homepage(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_html_render(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text':  'A new list item'}
            )
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = home_page(request)

        self.assertIn('A new list item', response.content.decode())
