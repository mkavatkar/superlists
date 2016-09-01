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
        result_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), result_html)
