# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import query
from django.db import models

from caching.base import CachingQuerySet


class RecipeQuerySet(CachingQuerySet, query.QuerySet):

    def published_recipes(self):
        return self.filter(large_image__isnull=False)

    def latest(self):
        return self.order_by('-last_updated')

    def recipes_startswith(self, text):
        return self.filter(name__istartswith=text)

class RecipeManager(models.Manager):
    def get_queryset(self):
        return RecipeQuerySet(self.model, using=self._db)

    def published_recipes(self):
        return self.get_queryset().published_recipes()

    def latest(self):
        return self.get_queryset().latest()

    def recipes_startswith(self, text):
        return self.get_queryset().recipes_startswith()
