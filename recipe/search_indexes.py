#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elasticsearch_dsl import DocType, Integer, String, Date, Nested, Boolean, analyzer

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "snowball", "stop"],
    char_filter=["html_strip"]
)

class RecipeIndex(DocType):
    document_id = Integer(index='not_analyzed')
    name = String(analyzer=html_strip)
    preparation_time = Integer(index='not_analyzed')

    ingredients = String(analyzer=html_strip)
    servings = Integer(index='not_analyzed')
    likes = Integer(index='not_analyzed')
    source_text = String()
    slug = String(index='no')
    source_slug = String(index='not_analyzed')
    large_image = String(index='no')
    last_updated = Date(index='not_analyzed')

    courses = String()
    cuisines = String()
    holidays = String()

    class Meta:
        index = 'recipe'
