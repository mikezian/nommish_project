#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import make_option
import datetime
import urllib

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

from django.core.management import call_command
from django.core.management.base import BaseCommand

from yummly import Client

from recipe.models import Recipe, Course, Cuisine, Holiday, UserCollection, RecipesCollection


class Command(BaseCommand):
    args = 'No arguments needed'
    help = 'Command to sync recipes from Yummly API'

    def add_arguments(self, parser):
        parser.add_argument('--start',
            dest='start',
            default=0,
            help='')
        
        parser.add_argument('--max_results',
            dest='max_results',
            default=490,
            help='')


    def handle(self, *args, **options):
        self.stdout.write('success')
        params = {
            'q': '',
            'maxResult': options.get('max_results'),
            'start': options.get('start'),
            'requirePictures': 'true'
        }
        # course = 'Main Dishes'
        # course = 'course^course-{}'.format(course)
        # params.update({'allowedCourse[]': course})
        current_date = datetime.date.today()
        current_date = current_date.strftime('%Y%m%d')
        key = 'syncrecipe::%s' % current_date
        c = Client(
                api_id=settings.YUMMLY_APP_KEY,
                api_key=settings.YUMMLY_API_KEY
        )
        ctr = 1
        res = c.search(**params)
        for item in res.matches:
            ctr = cache.get(key, 1)
            if Recipe.objects.filter(recipe_source_id=item.id).first():
                print 'recipe already stored ', item.id
                continue
            if ctr > 480:
                print 'Exiting: Yummly quota limit'
                return
            recipe = c.recipe(item.id)
            recipe_info = {
                'recipe_source_id': item.id,
                'name': item.recipeName,
                'ingredients': list(recipe.ingredientLines),
                'attribution_text': recipe.attribution.text,
                'attribution_url': recipe.source.sourceSiteUrl,
                'source_text': item.sourceDisplayName,
                'source_url': recipe.source.sourceSiteUrl,
                'large_image': recipe.images[0]['hostedLargeUrl'],
                'small_image': recipe.images[0]['hostedSmallUrl'],
                'url': recipe.source.sourceRecipeUrl,
                'preparation_time': recipe.totalTimeInSeconds if recipe.totalTimeInSeconds else 1,
                'servings': recipe.numberOfServings if recipe.numberOfServings else 1,
                'json_response': recipe
            }
            recipe = Recipe.objects.get_or_create(**recipe_info)[0]
            try:
                if item.attributes.get('holiday', None):
                    print 'holiday', item.attributes
                    for attr in item.attributes.get('holiday'):
                        recipe_holiday = Holiday.objects.get(name=attr)
                        recipe.holidays.add(recipe_holiday)
            except ObjectDoesNotExist as e:
                print 'holiday err: ', e.message, item.id, attr
            except IntegrityError as e:
                print 'holiday err: ', e.message, item.id
            finally:
                print 'done holiday'

            try:
                if item.attributes.get('course', None):
                    for attr in item.attributes.get('course'):
                        recipe_course = Course.objects.get(name=attr)
                        recipe.courses.add(recipe_course)
            except ObjectDoesNotExist as e:
                print 'course err: ', e.message, item.id, attr
            except IntegrityError as e:
                print 'course err: ', e.message, item.id, attr
            finally:
                print 'done course'

            try:
                if item.attributes.get('cuisine', None):
                    for attr in item.attributes.get('cuisine'):
                        recipe_cuisine = Cuisine.objects.get(name=attr)
                        recipe.cuisines.add(recipe_cuisine)
            except ObjectDoesNotExist as e:
                print 'cuisine err: ', e.message, item.id, attr
            except IntegrityError as e:
                print 'cuisine err: ', e.message, item.id, attr
            finally:
                print 'done cuisine'
            cache.set(key, ctr + 1)
        print "total recipes", res.totalMatchCount
        call_command('index_recipes', verbosity=3, interactive=False)