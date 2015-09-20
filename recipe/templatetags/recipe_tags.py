#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django import template
from ..models import Course

register = template.Library()

@register.inclusion_tag('_top_slider.html')
def top_slider_contents():
    return {'slider_contents': [
            {
                'img_link': 'img/italian-cuisine.jpg',
                'caption': 'Looking for Italian Cuisine?',
                'link_caption': 'ITALIAN',
                'link': reverse('cuisine-list', kwargs={'slug': 'italian'}),
            },
            {
                'img_link': 'img/dessert-course.jpg',
                'caption': 'Sweet Treats',
                'link_caption': 'DESSERTS',
                'link': reverse('course-list', kwargs={'slug': 'deserts'}),
            }
        ]
    }
@register.inclusion_tag('_recipe_course_list.html')
def recipe_course_list():
    course_list = ['Breakfast and Brunch', 'Main Dishes', 'Desserts', 'Lunch and Snacks', 'Beverages', 'Salads', 'Side Dishes']
    courses = Course.objects.filter(name__in=course_list).all()
    return {'courses': courses}