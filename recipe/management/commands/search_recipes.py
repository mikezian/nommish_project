#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from elasticsearch_dsl import search
from elasticsearch import Elasticsearch

# Q - shortcut for Query
# A - shortcut for Aggregation
from elasticsearch_dsl.query import MultiMatch, Q#, A

es = Elasticsearch([
    {'host': 'localhost', 'port': 9200},
])


class Command(BaseCommand):
    args = 'No arguments needed'
    help = 'Command to test search recipe index'

    def handle(self, *args, **options):
        s = search.Search(using=es, index='recipe')
        keyword = 'roasted chicken'
        keyword2 = [{"span_term": {"name": k}} for k in keyword.split()]
        s.update_from_dict({
            'query': {
                'bool': {
                    'must': [
                        {
                            'multi_match': {
                                'query': {
                                    'query': keyword,
                                    'fields': ['name^2', 'ingredients'],
                                    'slop': 2
                                },
                            },
                        },
                        {
                            'term': {'courses': '1'}
                        }
                    ]
                }
            },
            "aggs" : {
                "all_courses": {
                    "terms" : { "field" : "courses" }
                }
            }

        })
        response = s.execute()
        for item in response:
            print item.name, item.meta.score#, item.meta.explanation.details, item.meta.explanation.value
            print item.ingredients.join(', '), item.courses
            print '==='
        print len(response)

        print s.to_dict()