from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from recipe.models import *

class TestLoggedUsers(TestCase):
    fixtures = ['recipe/fixtures/test_data.json']

    # fixtures = ('test_data.json', )

    def setUp(self):
        self.user = User.objects.create_user('test_user', 'user@test.net', 'secret')
        self.user.save()
        self.client = Client()
        print "welcome in setup: while..nothing to setup.."


    def tearDown(self):
        self.user.delete()

    def test_logged_user_collection_page(self):
        response = self.client.get(reverse('user-recipe-collection'), follow=True)
        self.assertContains(response, '<h2>Sign In</h2>')
        self.client.login(username='test_user', password='secret')
        response = self.client.get(reverse('user-recipe-collection'), follow=True)
        self.assertContains(response, 'My Collection')
