# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import query


class RecipeQuerySet(query.QuerySet):
    def published_recipes(self):
        return self.filter(large_image__isnull=False)

    def latest(self):
        return self.order_by('-last_updated')

    def recipes_startswith(self, text):
        return self.filter(name__istartswith=text)

RecipeManager = RecipeQuerySet.as_manager
