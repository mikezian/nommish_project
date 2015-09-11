#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import jsonfield
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from slugify import slugify

def slugify_url_hash(title, max_length):
    h = hashlib.sha1()
    h.update(str(time.time()))
    _title = slugify(title)[:39]
    print 'slug', '%s-%s' % (_title, h.hexdigest()[:10])
    return '%s-%s' % (_title, h.hexdigest()[:10])

class Profile(models.Model):
    # one-one relation with user
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        related_name='profile',
        verbose_name='user'
    )
    first_name = models.CharField('First Name', max_length=500, null=True)
    last_name = models.CharField('First Name', max_length=500, null=True)
    # object manager
    # objects = managers.ProfileManager()

    @property
    def username(self):
        return self.username

    class Meta:
        db_table = 'nommish_userprofile'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ('user',)

    def __str__(self):
        return self.user.username

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


class Cuisine(models.Model):
    CUISINE_CHOICES = (
        ('1', 'American'),
        ('2', 'Italian'),
        ('3', 'Asian'),
        ('4', 'Mexican'),
        ('5', 'Southern & Soul Food'),
        ('6', 'French'),
        ('7', 'Southwestern'),
        ('8', 'Barbecue'),
        ('9', 'Indian'),
        ('10', 'Chinese'),
        ('11', 'Cajun & Creole'),
        ('12', 'English'),
        ('13', 'Mediterranean'),
        ('14', 'Greek'),
        ('15', 'Spanish'),
        ('16', 'German'),
        ('17', 'Thai'),
        ('18', 'Moroccan'),
        ('19', 'Irish'),
        ('20', 'Japanese'),
        ('21', 'Cuban'),
        ('22', 'Hawaiian'),
        ('23', 'Swedish'),
        ('24', 'Hungarian'),
        ('25', 'Portugese'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, choices=CUISINE_CHOICES, default='1')
    slug = models.SlugField(db_index=True, null=True)
    cover = models.TextField(null=True)

    class Meta:
        db_table = 'nommish_cuisine'

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(self.name)
        super(Cuisine, self).save(*args, **kwargs)


class Course(models.Model):
    COURSE_CHOICES = (
        ('1', 'Main Dishes'),
        ('2', 'Desserts'),
        ('3', 'Side Dishes'),
        ('4', 'Lunch and Snacks'),
        ('5', 'Appetizers'),
        ('6', 'Salads'),
        ('7', 'Breads'),
        ('8', 'Breakfast and Brunch'),
        ('9', 'Soups'),
        ('10', 'Beverages'),
        ('11', 'Condiments and Sauces'),
        ('12', 'Cocktails'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, choices=COURSE_CHOICES, default='1')
    slug = models.SlugField(db_index=True, null=True)
    cover = models.TextField(null=True)

    class Meta:
        db_table = 'nommish_course'

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

class Holiday(models.Model):
    HOLIDAY_CHOICES = (
        ('1', 'Christmas'),
        ('2', 'Summer'),
        ('3', 'Thanksgiving'),
        ('4', 'New Year'),
        ('5', 'Super Bowl / Game Day'),
        ('6', 'Halloween'),
        ('7', 'Hanukkah'),
        ('8', '4th of July')
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, choices=HOLIDAY_CHOICES, default='1')
    slug = models.SlugField(db_index=True, null=True)
    cover = models.TextField(null=True)

    class Meta:
        db_table = 'nommish_holiday'

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(self.name)
        super(Holiday, self).save(*args, **kwargs)

class UserCollectionManager(models.Manager):
    def create_or_addto_collection(self, collection, user, recipe=None):
        """
        This method create new user collection if it passes only the name
        and add the recipe to the collection if recipe instance is passed.
        """
        if not isinstance(collection, UserCollection):
            collection = UserCollection.objects.create(name=collection, user=user)
            if not recipe:
                return collection
            collection.cover = recipe.large_image
            collection.save()
            rc = RecipesCollection.objects.create(collection=collection, recipe=recipe)
            return collection

        collection = UserCollection.objects.get(user=user, id=collection.id)
        collection.cover = recipe.large_image
        collection.save()
        rc = RecipesCollection.objects.create(collection=collection, recipe=recipe)
        return rc

    def remove_from_collection(self, collection, user, recipe):
        """
        This method deletes recipe from recipe collection.
        """
        collection = UserCollection.objects.get(user=user, id=collection)
        rc = RecipesCollection.objects.filter(collection=collection, recipe_id=recipe)
        rc.delete()
        return rc

class UserCollection(models.Model):
    name = models.CharField(max_length=2000, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='collections', related_name='collections')
    date_created = models.DateTimeField(auto_now=True)
    slug = models.SlugField(db_index=True, null=True)
    cover = models.TextField(null=True)
    objects = UserCollectionManager()

    class Meta:
        db_table = 'nommish_user_collection'

    @classmethod
    def user_collection_count(cls, user):
        collections = cls.objects.filter(user=user)\
            .values('name', 'slug', 'cover')\
            .annotate(count=models.Count('user_collections'))
        return collections

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            self.slug = slugify_url_hash(self.name, 50)
        super(UserCollection, self).save(*args, **kwargs)

from .managers import RecipeManager


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    recipe_source_id = models.CharField(max_length=4000, unique=True)
    name = models.CharField(max_length=2000)
    ingredients = models.TextField(null=True)
    attribution_text = models.CharField(max_length=2000)
    attribution_url = models.TextField(null=True)
    source_text = models.TextField(null=True)
    source_url = models.TextField(null=True)
    large_image = models.TextField(null=True)
    small_image = models.TextField(null=True)
    url = models.TextField()
    preparation_time = models.IntegerField(default=60)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    servings = models.IntegerField(default=1)
    json_response = jsonfield.JSONField(null=True)
    is_indexed = models.NullBooleanField(default=False, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    courses = models.ManyToManyField(Course, verbose_name='courses', related_name='courses')
    cuisines = models.ManyToManyField(Cuisine, verbose_name='cuisines', related_name='cuisines')
    holidays = models.ManyToManyField(Holiday, verbose_name='holidays', related_name='holidays')
    slug = models.SlugField(db_index=True, null=True)
    source_slug = models.SlugField(db_index=True, null=True)
    objects = RecipeManager()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'nommish_recipe'

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            self.slug = slugify_url_hash(self.name, 50)
        if not self.source_slug:
            self.source_slug = slugify(self.source_text)[:50]
        super(Recipe, self).save(*args, **kwargs)

class RecipesCollection(models.Model):
    collection = models.ForeignKey(UserCollection, verbose_name='user_collections', related_name='user_collections', default=None)
    recipe = models.ForeignKey(Recipe, verbose_name='recipes', related_name='recipes')
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'nommish_recipe_collection'
        unique_together = (("collection", "recipe"),)

