#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections

from recipe.models import Recipe
from recipe.search_indexes import RecipeIndex

es = Elasticsearch([
    {'host': 'localhost', 'port': 9200},
])

connections.add_connection(alias='default', conn=es)

class Command(BaseCommand):
    args = 'No arguments needed'
    help = 'Command to index recipe to elasticsearch'

    def handle(self, *args, **options):
        if not es.indices.exists('recipe'):
            RecipeIndex.init()
        recipes = Recipe.objects.only(
            'id',
            'name',
            'preparation_time',
            'ingredients',
            'servings',
            'likes',
            'source_text',
            'last_updated',
            'slug',
            'courses',
            'cuisines',
            'holidays',
        ).all()
        for recipe in recipes:
            data = {
                'document_id': recipe.id,
                'name': recipe.name,
                'preparation_time': recipe.preparation_time,
                'ingredients': recipe.ingredients,
                'servings': recipe.servings,
                'likes': recipe.likes,
                'source_text': recipe.source_text,
                'slug': recipe.slug,
                'source_slug': recipe.source_slug,
                'large_image': recipe.large_image,
                'last_updated': recipe.last_updated,
                'courses': [course.id for course in recipe.courses.all()] if len(recipe.courses.all()) else None,
                'holidays': [holiday.id for holiday in recipe.holidays.all()] if len(recipe.holidays.all()) else None,
                'cuisines': [cuisine.id for cuisine in recipe.cuisines.all()] if len(recipe.cuisines.all()) else None,
            }
            idx = RecipeIndex(**data)
            idx.meta.id = recipe.id
            idx.save()
            recipe.is_indexed = True
            recipe.save()
