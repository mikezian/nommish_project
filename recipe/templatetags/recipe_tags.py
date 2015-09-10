#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
from ..models import Course

register = template.Library()

@register.inclusion_tag('_recipe_course_list.html')
def recipe_course_list():
    courses = Course.objects.all()
    return {'courses': courses}
