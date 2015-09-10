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
        # s = Search(using=es)
        # q = Q("match", query='herbed chicken', fields=['name', 'ingredients^2'], minimum_should_match="100%")
        # s.query = q
        # s.filter('term', ingredients='herbed')
        # s.filter('term', ingredients='chicken')

        # s = s.extra(size=2000)
        # s = s.extra(explain=True)
        s = search.Search(using=es, index='recipe')
        keyword = 'roasted chicken'
        keyword2 = [{"span_term": {"name": k}} for k in keyword.split()]
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-function-score-query.html
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html#type-cross-fields
        # 'multi_match': {
        #     'query': keyword,
        #     'fields': ['name', 'ingredients^2'],
        #     'fuzziness': 2,
        #     'type': 'most_fields',
        # },
        # 'field_value_factor': {
        #     'field': 'likes',
        #     'factor': 0.2
        # },
        # 'boost_mode': 'sum'
        # 'query': {
        #     "filtered": {
        #         "query": {
        #             'match': {
        #                 'name': {'query': keyword, 'type': 'phrase_prefix', 'slop': 0}
        #             },
        #         },
        #         "filter": {
        #             "term": {
        #                 "courses": "1"
        #             }
        #         }
        #     }
        # }
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
        print s
        print s.to_dict()
        # s.sort('_score,ingredients:desc')
        response = s.execute()
        for item in response:
            print item.name, item.meta.score#, item.meta.explanation.details, item.meta.explanation.value
            print item.ingredients.join(', '), item.courses
            print '==='
        print len(response)

        print s.to_dict()