#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from recipe.models import Recipe, Course, Cuisine, Holiday


class Command(BaseCommand):
    args = 'No arguments needed'
    help = 'Command to sync Holiday, Course, Cuisine Collection cover image'

    def handle(self, *args, **options):
        collections = [Holiday, Course, Cuisine]
        for collection in collections:
            items = collection.objects.all()
            for item in items:
                filters = {
                    '%ss__id' % collection._meta.verbose_name: item.id
                }
                recipe = Recipe.objects.filter(**filters).order_by('-last_updated')
                if not recipe:
                    print 'continue %s' % recipe
                    continue
                item.cover = recipe[0].large_image
                item.save()

        # items = Course.objects.all()
        # for item in items:
        #     print item, item.id
        #     recipe = Recipe.objects.filter(courses__id=item.id).order_by('-last_updated')
        #     if not recipe:
        #         continue
        #     item.cover = recipe[0].large_image
        #     item.save()


        # items = Cuisine.objects.all()
        # for item in items:
        #     print item, item.id
        #     recipe = Recipe.objects.filter(cuisines__id=item.id).order_by('-last_updated')
        #     if not recipe:
        #         continue
        #     item.cover = recipe[0].large_image
        #     item.save()
