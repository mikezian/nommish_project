from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from recipe.models import *

class TestModels(TestCase):
    fixtures = ['recipe/fixtures/test_data.json']


    def test_recipe_count(self):
        recipe = Recipe.objects.all()
        self.assertEquals(len(recipe), 26)
