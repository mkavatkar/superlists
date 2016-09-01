from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page


# Create your tests here.
class HomepageTest(TestCase):
    def test_root_url_resolves_to_homepage(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
