#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
# from csv import reader
import ast


register = template.Library()
def to_str(uni_or_str):
    if isinstance(uni_or_str, unicode):
        return uni_or_str.encode('utf-8')
    else:
        return uni_or_str

@register.filter(name='prettify_time_in_seconds')
def prettify_time_in_seconds(sec):
    if sec < 60:
        return 'less than 5 mins.'
    minute, seconds = divmod(sec, 60)
    hours, minute = divmod(minute, 60)

    if hours:
        if minute > 0:
            return '%s h. %s m.' % (hours, minute)
        return '%s h.' % hours
    return '%s m.' % minute

@register.filter(name='format_ingredients')
def format_ingredients(ingredients):
    # https://stackoverflow.com/questions/1894269/convert-string-representation-of-list-to-list-in-python
    return set([i for i in ast.literal_eval(ingredients)])

@register.filter
def join_list(object):
    return ', '.join([object.get('name') for o in object])

@register.filter
def pagination_limited_page_range(object, current_page):
    """
    This filter partition pagination links by page_range
    e.g 1-5 6-10 11-15 etc
    """
    page_range = 5
    remainder = abs(current_page % page_range)
    if current_page < page_range or not remainder:
        if not remainder:
            return object[current_page-page_range:current_page]
        if current_page == 1:
            return object[current_page-1:page_range]
        return object[current_page-remainder:page_range]
    else:
        if remainder < page_range:
            return object[(current_page - remainder):current_page+(page_range - remainder)]
        return object[(current_page - remainder):(current_page+(page_range - remainder - 1))]

# https://stackoverflow.com/questions/1107737/numeric-for-loop-in-django-templates
@register.filter(name='loop_range') 
def loop_range(number):
    return range(1, number+1)

# https://stackoverflow.com/questions/2047622/how-to-paginate-django-with-other-get-variables
@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()