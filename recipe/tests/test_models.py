from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from recipe.models import *

class TestModels(TestCase):
    fixtures = ['recipe/fixtures/test_data.json']

    def setUp(self):
        self.user = User.objects.create_user('test_user', 'user@test.net', 'secret')
        self.user.save()
        self.client = Client()

    def test_recipe_count(self):
        recipe = Recipe.objects.all()
        self.assertEquals(len(recipe), 26)

    def test_recipe_to_collection(self):
        recipe = Recipe.objects.get(pk=29368)
        current_likes = recipe.likes
        collection = UserCollection.objects.create_or_addto_collection('my collection', self.user, recipe=recipe)
        # test if the latest collection cover gets the latest recipe added
        self.assertEquals(collection.cover, recipe.large_image)
        # test if the recipe likes was incremented
        self.assertEquals(recipe.likes, current_likes + 1)
        collection = UserCollection.objects.remove_from_collection(collection=collection.id, user=self.user, recipe=recipe)
        # check likes if it has been decremented
        self.assertEquals(recipe.likes, current_likes)
        self.assertEquals(len(collection), 0)